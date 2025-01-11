import os

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
from keyboards.inline.fanlar import (
    fanlar_inline_keyboard,
    til_inline_keyboard,
    baza_inline_keyboard,
    tasdiqlash_inline_keyboard,
)
load_dotenv()

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


@dp.message_handler(lambda message: message.text == "📝 Test Buyurtma")
async def start_test_buyurtma(message: types.Message):
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
            f"🔎 Buyurtma ma'lumotlari:\n"
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
            is_correct = int(balance) - int(data['kitobcha_soni'] * 2900)
        else:
            await call.message.answer(f"Ma'lumotlaringizni olishda muammo bo'ldi🤔")
        if is_correct > 0:
            get_data = {
              "number_books": data['kitobcha_soni'],
              "database_type": data['baza'],
              "subject1": (data['soha']).split('-')[0],
              "subject2": (data['soha']).split('-')[1],
              "language": data['til'],
              "user": 12
            }
            await call.message.edit_text(f"✅ Buyurtma tasdiqlandi!")
            url = os.getenv("TEST_BUYURTMA_POST")
            req = requests.post(url, data=get_data)

            if req.status_code == 200:
                req_patch = requests.patch(f'{url_user_patch}{call.from_user.id}', data={'balans': is_correct})
                await call.message.answer(req_patch.status_code)
                await call.message.answer("Test tayyor")
            else:
                await call.message.answer("Xatolik")
        else:
            await call.message.answer("Balansingizda yetarlicha mablag' mavjud emas!\nHisobingizni to'lding va davom eting.\nTalabalik sari olg'a🎓📚✨")
        await state.finish()
    elif call.data == "bekor":
        await call.message.edit_text("❌ Buyurtma bekor qilindi.")
        await state.finish()
