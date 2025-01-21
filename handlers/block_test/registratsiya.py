from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ContentType
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import timedelta, datetime
from dotenv import load_dotenv

from keyboards.button.blok_test import blok_test_keyboard
from keyboards.button.test_tekshir_ortga_qaytish import ortga_qaytish
from loader import dp
from keyboards.button.main_kyb import main_keyboard
import os
import re
import requests

load_dotenv()


# Foydalanuvchi holatini kuzatish uchun State sinfi
class RegistrationStates(StatesGroup):
    ism_familiya = State()
    telefon_raqam = State()
    viloyat = State()
    fan1 = State()  # 1-fan tanlash
    fan2 = State()  # 2-fan tanlash
    rejalashtirilgan_vaqt = State()
    confirm = State()


# Har yakshanba ro'yxatdan o'tish eslatmasi
def get_next_sunday():
    today = datetime.now().date()
    days_to_sunday = (6 - today.weekday()) % 7
    # Agar bugun Yakshanba bo'lsa, 7 kun qo'shamiz
    if days_to_sunday == 0:
        days_to_sunday = 7
    next_sunday = today + timedelta(days=days_to_sunday)
    sunday = str(next_sunday)
    day, month, year = sunday.split('-')[2], sunday.split('-')[1], sunday.split('-')[0][2:]
    date = f"{day}.{month}.{year}"
    return date


def format_phone_number(phone_number):
    # Faqat raqamlarni olish uchun belgilarni tozalash
    digits = re.sub(r'\D', '', phone_number)

    # Raqam uzunligi tekshiriladi
    if len(digits) == 12 and digits.startswith("998"):
        # Namunadagi formatga keltirish
        formatted = f"+998 {digits[3:5]} {digits[5:8]} {digits[8:10]} {digits[10:]}"
    else:
        raise ValueError("Noto'g'ri telefon raqami formati")

    return formatted


# Inline viloyatlar va fanlar
viloyatlar = ["Andijon", "Buxoro", "Jizzax", "Qashqadaryo", "Navoiy", "Namangan", "Samarqand", "Sirdaryo",
              "Surxondaryo", "Farg'ona", "Xorazm", "Toshkent", "Toshkent shahri", "Qoraqalpog'iston Respublikasi"]
fanlar = ['Matematika', 'Fizika', 'Kimyo', 'Biologiya', 'Tarix', 'Geografiya', 'Ingliz tili', 'Ona tili va adabiyot',
          'Huquq']
vaqt_intervallari = ['08:00 - 11:00', '10:00 - 13:00', '14:00 - 17:00', '18:00 - 21:00', '20:00 - 23:00']


@dp.message_handler(lambda message: message.text == "📋 Ro'yxatdan o'tish")
async def register_start(message: types.Message):
    user_id = message.from_user.id
    url_get = os.getenv("BLOK_TEST_GET")
    req_get = requests.get(f"{url_get}{user_id}")
    if req_get.status_code == 200:
        status_date = True
        for date in req_get.json():
            if get_next_sunday() == date['rejalashtirilgan_vaqt'].split("⏰")[0][1:].strip():
                status_date = False
                user_date = date['rejalashtirilgan_vaqt']
                await message.answer(f"Siz  {user_date}  blok test uchun ro'yxatdan o'tgansiz 😊")
        if status_date:
            await RegistrationStates.ism_familiya.set()
            await message.answer("Ism va familiyangizni kiriting", reply_markup=ortga_qaytish())
    else:
        await RegistrationStates.ism_familiya.set()
        await message.answer("Ism va familiyangizni kiriting", reply_markup=ortga_qaytish())


@dp.message_handler(state=RegistrationStates.ism_familiya)
async def get_name(message: types.Message, state: FSMContext):
    if message.text == '🔙 Ortga Qaytish':
        await message.answer("Blok test bo'limidasiz", reply_markup=blok_test_keyboard())
        await state.finish()
        return
    else:
        await state.update_data(ism_familiya=message.text)
        await RegistrationStates.telefon_raqam.set()

        # Telefon raqami tugmasi
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button = KeyboardButton(text="📲 Telefon raqamingizni yuboring", request_contact=True)
        keyboard.add(button)

        # Telefon raqami so'rovi
        await message.answer(
            "Telefon raqamingizni kiriting: (+998 XX XXX XX XX) yoki quyidagi tugma orqali yuboring.",
            reply_markup=keyboard
        )


@dp.message_handler(content_types=[ContentType.TEXT, ContentType.CONTACT], state=RegistrationStates.telefon_raqam)
async def get_phone(message: types.Message, state: FSMContext):
    if message.content_type == ContentType.CONTACT:
        contact = message.contact
        phone_number = contact.phone_number
    elif message.content_type == ContentType.TEXT:
        phone_number = message.text
        # Telefon raqamini tekshirish
        if not phone_number.startswith('+') and not phone_number.startswith('998'):
            await message.answer("Telefon raqamingiz noto'g'ri ko'rinadi. Iltimos, qayta kiriting.")
            return
    else:
        await message.answer("Telefon raqamingizni noto'g'ri yubordingiz. Iltimos, qayta urinib ko'ring.")
        return

    await state.update_data(telefon_raqam=phone_number)

    tel_raqam = await message.answer("Telefon raqamingiz qabul qilindi!", reply_markup=types.ReplyKeyboardRemove())

    # Keyingi holat: Viloyatni tanlash
    await RegistrationStates.viloyat.set()
    await tel_raqam.delete()
    # Viloyatlarni ko'rsatish
    inline_viloyatlar = InlineKeyboardMarkup(row_width=2)
    for viloyat in viloyatlar:  # Viloyatlar ro'yxati
        inline_viloyatlar.insert(InlineKeyboardButton(viloyat, callback_data=viloyat))

    await message.answer("Viloyatingizni tanlang", reply_markup=inline_viloyatlar)


@dp.callback_query_handler(state=RegistrationStates.viloyat)
async def get_region(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(viloyat=call.data)
    await call.message.edit_reply_markup(reply_markup=None)  # Tugmalarni olib tashlash
    await call.message.delete()  # Eski xabarni o‘chirish
    await RegistrationStates.fan1.set()
    await show_subject_selection(call.message, state, "1-fan")


async def show_subject_selection(message: types.Message, state: FSMContext, fan_number: str):
    inline_fanlar = InlineKeyboardMarkup(row_width=2)
    for fan in fanlar:
        inline_fanlar.insert(InlineKeyboardButton(fan, callback_data=fan))

    await message.answer(f"{fan_number}ni tanlang", reply_markup=inline_fanlar)


@dp.callback_query_handler(state=RegistrationStates.fan1)
async def get_fan1(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(fan1=call.data)
    await call.message.edit_reply_markup(reply_markup=None)  # Tugmalarni olib tashlash
    await call.message.delete()  # Eski xabarni o‘chirish

    # Endi 2-fanni tanlashga o'tamiz
    await RegistrationStates.fan2.set()
    await show_subject_selection(call.message, state, "2-fan")


@dp.callback_query_handler(state=RegistrationStates.fan2)
async def get_fan2(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(fan2=call.data)
    await call.message.edit_reply_markup(reply_markup=None)  # Tugmalarni olib tashlash
    await call.message.delete()  # Eski xabarni o‘chirish

    # Vaqtni tanlashga o'tamiz
    await show_time_selection(call.message, state)


async def show_time_selection(message: types.Message, state: FSMContext):
    inline_vaqt = InlineKeyboardMarkup(row_width=2)
    for vaqt in vaqt_intervallari:
        inline_vaqt.add(InlineKeyboardButton(vaqt, callback_data=vaqt))

    await RegistrationStates.rejalashtirilgan_vaqt.set()
    await message.answer("Qaysi vaqtda topshirmoqchisiz", reply_markup=inline_vaqt)


@dp.callback_query_handler(state=RegistrationStates.rejalashtirilgan_vaqt)
async def get_schedule(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(rejalashtirilgan_vaqt=call.data)
    await call.message.edit_reply_markup(reply_markup=None)  # Tugmalarni olib tashlash
    await call.message.delete()  # Eski xabarni o‘chirish

    user_data = await state.get_data()
    summary = f"""📋 Sizning ma’lumotlaringiz\n
👤 Ism: {user_data['ism_familiya']}
📞 Telefon: {user_data['telefon_raqam']}
📍 Viloyat: {user_data['viloyat']}
📚 1-fan: {user_data['fan1']}
📚 2-fan: {user_data['fan2']}
🗓 Vaqt: {user_data['rejalashtirilgan_vaqt']}
"""
    confirm_btn = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Tasdiqlash", callback_data="confirm_"),
        InlineKeyboardButton("❌ Bekor qilish", callback_data="cancel_")
    )
    await call.message.answer(summary, reply_markup=confirm_btn)
    await RegistrationStates.confirm.set()


@dp.callback_query_handler(lambda c: c.data == 'confirm_', state=RegistrationStates.confirm)
async def confirm_registration(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    user_id = call.from_user.id
    phone_number = format_phone_number(user_data['telefon_raqam'])
    url_post = os.getenv('BLOK_TEST_POST')
    req = requests.post(url_post, data={"telegram_id": user_id,
                                        "ism_familiya": user_data['ism_familiya'],
                                        "telefon_raqam": phone_number,
                                        "viloyat": user_data['viloyat'],
                                        "fan1": user_data['fan1'],
                                        "fan2": user_data['fan2'],
                                        "rejalashtirilgan_vaqt": f"📅 {get_next_sunday()} ⏰ {user_data['rejalashtirilgan_vaqt']}",
                                        "status": "kutmoqda"})
    if req.status_code == 200:
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.delete()
        await call.message.answer("✅ Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!", reply_markup=main_keyboard())
        await call.message.answer(
            f"Sizga {get_next_sunday()} kuni soat {user_data['rejalashtirilgan_vaqt'][:5]} da test materiallari yuboriladi, belgilangan vaqt ichida javoblarni yuborishingizni so'rab qolamiz!\nIlmiz ziyoda bo'lsin!")
    else:
        await call.message.edit_reply_markup(reply_markup=None)
        await call.message.delete()
        await call.message.answer("Ro'yxatdan o'tishda xatolik")
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'cancel_', state=RegistrationStates.confirm)
async def cancel_registration(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.delete()
    await call.message.answer("❌ Ro‘yxatdan o‘tish bekor qilindi.", reply_markup=main_keyboard())
    await state.finish()
