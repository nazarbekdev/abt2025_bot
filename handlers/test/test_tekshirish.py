import asyncio
import time
import ast
import aiohttp
import os

import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from loader import dp, bot
from keyboards.inline import tekshirish_usullari


@dp.message_handler(lambda message: message.text == "✅ Test Tekshirish")
async def test_tekshirish(message: Message):
    msg = await message.answer("Qaysi usulda tekshirmoqchisiz?", reply_markup=tekshirish_usullari.tekshirish_usullari())
    await asyncio.sleep(7)
    await msg.delete()


@dp.callback_query_handler(lambda call: call.data == "titul")
async def tekshirish_titul(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("📸 Titul varaqangizni rasmga olib yuboring!\n\n❗️Natijangiz to'g'ri tekshirilishi uchun titulni rasmga olish qoidalariga amal qiling!")
    await call.answer()


@dp.message_handler(content_types=['photo'])
async def handle_photo(message: Message):
    api_url = os.getenv("CHECK_TITUL_POST")
    checking_msg = await message.answer("️♻️ Tekshirilmoqda...")

    # Telegram serveridan fayl ma'lumotlarini olish
    file_info = await bot.get_file(message.photo[-1].file_id)

    # Faylni yuklab olish
    downloaded_file = await bot.download_file(file_info.file_path)

    # Faylni vaqtinchalik saqlash
    with open("check_photo.jpg", "wb") as f:
        f.write(downloaded_file.read())

    # API'ga rasmni yuborish
    with open("check_photo.jpg", "rb") as image_file:
        files = {
            'file': image_file,
        }
        data = {
            'user': 12,
            'book_id': '',
        }

        response = requests.post(api_url, files=files, data=data)
    os.remove("check_photo.jpg")

    if response.status_code == 200:
        success_msg = await message.answer("✅ Muvaffaqiyatli tekshirildi!")
        time.sleep(2)
        await checking_msg.delete()
        await success_msg.delete()
        send_file_msg = await message.answer("📥 Fayl yuklanmoqda...")
        url = os.getenv("CHECK_TITUL_GET")

        # Yuklanadigan faylni API'dan olish
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            # Javob sarlavhalaridan Content-Disposition ni olish
            content_disposition = r.headers.get('Content-Disposition')
            if content_disposition:
                file_name = content_disposition.split('filename=')[-1].strip('"')
            else:
                file_name = 'downloaded_file.pdf'

            # Faylni saqlash uchun katalogni tekshirish va yaratish
            directory = os.path.dirname(file_name)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            # Faylni saqlash
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Xabarlarni o'chirish
            await send_file_msg.delete()

            # Faylni foydalanuvchiga yuborish
            await message.answer_document(open(file_name, 'rb'))

            # Faylni o'chirish
            os.remove(file_name)

        else:
            await message.answer("Faylni yuklab olishda xatolik yuz berdi.")
    else:
        msg = response.json()['message']
        if len(msg) > 40:
            await checking_msg.delete()
            await message.answer(f'🚫 Error: {msg}\n\n/id_bilan_tekshir')
        else:
            await checking_msg.delete()
            await message.answer(f'🚫 Error: {msg}')


class Form(StatesGroup):
    tekshirish_oddiy = State()


@dp.callback_query_handler(lambda call: call.data == "oddiy")
async def tekshirish_oddiy(call: CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("❗️ Javoblarni ushbu formatda jo'nating 👇")
    await call.message.answer("1234567*abcdabcdab...cd")
    await Form.tekshirish_oddiy.set()  # Holatni o'rnatamiz
    await call.answer()


# Faqat "tekshirish_oddiy" holatida kelgan xabarlarni ushlash
@dp.message_handler(state=Form.tekshirish_oddiy)
async def tekshirish(message: Message, state: FSMContext):
    user_msg = message.text
    book_id = user_msg.split('*')[0]
    user_keys = user_msg.split('*')[1].upper()
    if len(book_id) != 7:
        await message.answer('Kitob ID 7 xonadan iborat bo\'lishi kerak!')
        await state.finish()
    if len(user_keys) != 90:
        await message.answer('Javoblar kaliti 90 tadan iborat bo\'lishi kerak!')
        await state.finish()

    url_ans_data = os.getenv("ANSWER_DATA")
    data = requests.get(f'{url_ans_data}{book_id}')

    if data.status_code == 200:
        start_ = await message.answer("♻️ Tekshirishmoqda...")
        keys = data.json()['answers']
        keys = ast.literal_eval(keys)
        # Variables to track correct answers and scores
        mandatory_correct = fan1_correct = fan2_correct = 0
        mandatory_score = fan1_score = fan2_score = 0.0

        # Result formatting
        result = []
        for i, key in enumerate(keys, start=1):
            correct_answer = keys[i-1][str(i)]
            user_answer = user_keys[i - 1]

            # Check correctness and generate result line
            is_correct = correct_answer == user_answer
            mark = "✅" if is_correct else "❌"
            result.append(f"{i}. {user_answer} {mark}")

            # Calculate scores
            if is_correct:
                if 1 <= i <= 30:
                    mandatory_correct += 1
                    mandatory_score += 1.1
                elif 31 <= i <= 60:
                    fan1_correct += 1
                    fan1_score += 3.1
                elif 61 <= i <= 90:
                    fan2_correct += 1
                    fan2_score += 2.1

        # Calculate total score
        total_score = mandatory_score + fan1_score + fan2_score

        # Compile the output
        summary = f"\nKitob ID: {book_id}\n\nMajburiy fanlar: {mandatory_correct} ta\nFan1: {fan1_correct} ta\nFan2: {fan2_correct} ta\n\nUmumiy ball: {total_score:.1f}"

        result_output = "\n".join(result) + "\n\n" + summary
        await start_.delete()
        await message.answer(result_output)
    else:
        await message.answer('Bunday kitobcha mavjud emas!')
    await state.finish()
