import os
import io

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.button.test_buyurtma_kyb import test_buyurtma_keyboard
from keyboards.button.test_tekshir_ortga_qaytish import ortga_qaytish
from loader import dp, bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
from keyboards.inline.fanlar import (
    fanlar_inline_keyboard,
    til_inline_keyboard,
    baza_inline_keyboard,
    tasdiqlash_inline_keyboard,
)

load_dotenv()
ADMIN_ID = os.getenv('ADMINS')

# Sohalar, tillar va bazalar uchun lug'atlar
SOHALAR = {
    "5-9": "Tarix - Ona tili va Adabiyot",
    "5-11": "Tarix - Ingliz tili",
    "5-12": "Tarix - Huquq",
    "5-10": "Tarix - Geografiya",
    "12-11": "Huquq - Ingliz tili",
    "4-9": "Biologiya - Ona tili va Adabiyot",
    "4-8": "Biologiya - Kimyo",
    "8-7": "Kimyo - Matematika",
    "8-4": "Kimyo - Biologiya",
    "9-7": "Ona tili va Adabiyot - Matematika",
    "9-11": "Ona tili va Adabiyot - Ingliz tili",
    "7-6": "Matematika - Fizika",
    "7-11": "Matematika - Ingliz tili",
    "7-10": "Matematika - Geografiya",
    "7-9": "Matematika - Ona tili va Adabiyot",
    "6-7": "Fizika - Matematika",
    "6-11": "Fizika - Ingliz tili",
    "11-9": "Ingliz tili - Ona tili va Adabiyot",
    "13-5": "Rus tili - Tarix",
    "13-11": "Rus tili - Ingliz tili",
    "13-9": "Rus tili - Ona tili va Adabiyot",
}

TILLAR = {
    "1": "O'zbek tili",
    "2": "Rus tili",
}

BAZALAR = {
    "1": "Baza 1",
    "2": "Baza 2",
    "3": "Baza 3",
}


# Bosqichlarni belgilash
class TestBuyurtmaState(StatesGroup):
    soha = State()
    til = State()
    baza = State()
    kitobcha_soni = State()
    tasdiqlash = State()


@dp.message_handler(lambda message: message.text == "🔙 Ortga Qaytish", state="*")
async def cancel_and_restart(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Test yechish bo'limidasiz", reply_markup=test_buyurtma_keyboard())


@dp.message_handler(lambda message: message.text == "📝 Test Buyurtma")
async def start_test_buyurtma(message: types.Message):
    await message.answer('Test buyutma qilishda ketma-ketligiga amal qiling!', reply_markup=ortga_qaytish())
    await message.answer("O'z sohangizni tanlang!", reply_markup=fanlar_inline_keyboard())
    await TestBuyurtmaState.soha.set()


@dp.callback_query_handler(state=TestBuyurtmaState.soha)
async def choose_til(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(soha=call.data)
    await call.message.edit_text("Qaysi tilda tuzilsin?", reply_markup=til_inline_keyboard())
    await TestBuyurtmaState.til.set()


@dp.callback_query_handler(state=TestBuyurtmaState.til)
async def choose_baza(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(til=call.data)
    await call.message.edit_text("Bazani tanlang:", reply_markup=baza_inline_keyboard())
    await TestBuyurtmaState.baza.set()


@dp.callback_query_handler(state=TestBuyurtmaState.baza)
async def choose_kitobcha_soni(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(baza=call.data)
    await call.message.edit_text("Nechta kitobcha buyurtma qilmoqchisiz? (raqam kiriting)")
    await TestBuyurtmaState.kitobcha_soni.set()


@dp.message_handler(state=TestBuyurtmaState.kitobcha_soni)
async def confirm_order(message: types.Message, state: FSMContext):
    try:
        kitobcha_soni = int(message.text)
        await state.update_data(kitobcha_soni=kitobcha_soni)
        data = await state.get_data()


        soha = SOHALAR.get(data.get("soha"), "Noma'lum")
        til = TILLAR.get(data.get("til"), "Noma'lum")
        baza = BAZALAR.get(data.get("baza"), "Noma'lum")
        summa = kitobcha_soni * 2900

        await message.answer(
            f"🔖 Buyurtma ma'lumotlari:\n\n"
            f"📖 Soha: {soha}\n"
            f"🌐 Til: {til}\n"
            f"📚 Baza: {baza}\n"
            f"📄 Kitobcha soni: {kitobcha_soni}\n"
            f"💵 Buyurtma narxi: {summa} so'm\n\n"
            "Barchasini tasdiqlaysizmi?",
            reply_markup=tasdiqlash_inline_keyboard(),
        )
        await TestBuyurtmaState.tasdiqlash.set()
    except ValueError:
        await message.answer("Iltimos, kitobcha sonini raqam bilan kiriting.")


@dp.callback_query_handler(state=TestBuyurtmaState.tasdiqlash)
async def finalize_order(call: types.CallbackQuery, state: FSMContext):
    if call.data == "tasdiq":
        data = await state.get_data()
        url_user_info = os.getenv('USER_INFO')
        url_user_patch = os.getenv('USER_PATCH')
        req_info = requests.get(f'{url_user_info}{call.from_user.id}')

        if req_info.status_code == 200:
            balance = req_info.json()['balans']
            order = req_info.json()['order']
            is_correct = int(balance) - int(data['kitobcha_soni'] * 2900)
        else:
            await call.message.answer(f"Ma'lumotlaringizni olishda muammo bo'ldi 🤔")
        if is_correct > 0:
            get_data = {
              "number_books": data['kitobcha_soni'],
              "database_type": data['baza'],
              "subject1": (data['soha']).split('-')[0],
              "subject2": (data['soha']).split('-')[1],
              "language": data['til'],
              "user": 12
            }
            success_order = await call.message.edit_text(f"✅ Buyurtma tasdiqlandi!")
            url = os.getenv("TEST_BUYURTMA_POST")
            req = requests.post(url, data=get_data)

            if req.status_code == 200:
                req_patch = requests.patch(f'{url_user_patch}{call.from_user.id}', data={'balans': is_correct, 'order': order+1})
                if req_patch.status_code == 200:
                    success = await call.message.answer("Test tayyor")
                    url_file = os.getenv("TEST_DOWNLOAD_GET")
                    req_file = requests.get(url_file)
                    data = await state.get_data()

                    soha = SOHALAR.get(data.get("soha"), "Noma'lum")
                    if req_file.status_code == 200:
                        file_content = req_file.content
                        file_name = f"{soha}.pdf"

                        # Faylni yuborish
                        await bot.send_document(
                            chat_id=call.from_user.id,
                            document=types.InputFile(io.BytesIO(file_content), filename=file_name),
                            caption="❗️Diqqat. 3 soat vaqt belgilang va testni boshlang!\n\n© 2024 TestifyHub")
                        titul_path = os.getenv("TITUL_PATH")

                        if os.path.exists(titul_path):
                            await bot.send_document(
                                chat_id=call.from_user.id,
                                document=types.InputFile(titul_path),
                                caption="📄 Javoblarni belgilash uchun!"
                            )
                            await success_order.delete()
                            await success.delete()
                        else:
                            await call.message.answer("Titul fayli topilmadi 🤔")
                    else:
                        await call.message.answer("Server is not running!")
                else:
                    await call.message.answer("Nimadur xato bo'ldi 🤔")
            else:
                await call.message.reply("Qandaydir xatolik yuz berdi!\n🎟️ Buyurtmangiz ko'rib chiqish uchun yuborildi.")
                await bot.send_message(ADMIN_ID, f'❌❌❌❌❌❌❌\n\nFoydalanuvchi: {call.from_user.id}\n\n{get_data}\n\nUshbu buyurtma bajarilmadi!', )
        else:
            await call.message.answer("😔 Balansingizda yetarlicha mablag' mavjud emas!\n🔕 Tanaffusni unuting! Hisobingizni to‘ldiring va davom eting!")
            await call.message.answer("Siz albatta talaba bo'lasiz 😊")
        await state.finish()
    elif call.data == "bekor":
        await call.message.edit_text("❌ Buyurtma bekor qilindi.")
        await state.finish()
