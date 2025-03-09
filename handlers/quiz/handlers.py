import requests
import os
from pathlib import Path
from aiogram.types import Message
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from .states import QuizState
from loader import bot
from .api import get_subjects, get_databases, get_questions, save_result, notify_admins
from .keyboards import get_quiz_keyboard, get_fan_keyboard, get_baza_keyboard, get_options_keyboard
from keyboards.button.main_kyb import main_keyboard
from keyboards.button.back_button import back_keyboard
from .api import API_URL
from dotenv import load_dotenv
load_dotenv()

ADMIN = os.getenv("ADMINS")

# @dp.message_handler(lambda message: message.text == "🔙 Ortga Qaytish", state="*")
async def cancel_and_restart(message: types.Message):
    await message.answer("Asosiy bo'limdasiz", reply_markup=main_keyboard())
    return

# CallbackData uchun fabrika
quiz_callback = CallbackData("quiz", "action", "id")

# Quiz button handleri
async def quiz_button_handler(message: types.Message):
    await message.answer(
        "Assalomu alaykum, Fanlar bo‘yicha quiz testlar yechish uchun /quiz buyrug‘ini bosing!",
        reply_markup=back_keyboard()
    )

# /quiz buyrug‘i
async def cmd_quiz(message: types.Message, state: FSMContext):
    fans = get_subjects()
    if not fans:
        await message.answer("Hozircha fanlar mavjud emas!")
        return
    # Foydalanuvchining first_name ni saqlash
    user_name = message.from_user.first_name or "Nomalum"
    name = str(user_name)[:30]
    await state.update_data(user_name=name)
    
    await message.answer(
        "Quizni boshlash uchun fan tanlang:",
        reply_markup=get_fan_keyboard(fans)
    )
    await QuizState.choosing_fan.set()

# Fan tanlash
async def process_fan(callback_query: types.CallbackQuery, state: FSMContext):
    # Oldingi xabarni o‘chirish (fan tanlash xabari)
    try:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    except Exception as e:
        print(f"Xabarni o‘chirishda xatolik[process_fan]: {str(e)}")

    fan_id = callback_query.data.replace("fan_", "")
    await state.update_data(fan_id=fan_id)
    bazas = get_databases()
    if not bazas:
        await bot.answer_callback_query(callback_query.id, "Hozircha bazalar mavjud emas!")
        await state.finish()
        return
    await bot.send_message(
        callback_query.from_user.id,
        "Endi baza tanlang:",
        reply_markup=get_baza_keyboard(bazas)
    )
    await QuizState.choosing_baza.set()
    await bot.answer_callback_query(callback_query.id)

# Baza tanlash
async def process_baza(callback_query: types.CallbackQuery, state: FSMContext):
    # Oldingi xabarni o‘chirish (baza tanlash xabari)
    try:
        await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    except Exception as e:
        print(f"Xabarni o‘chirishda xatolik[process_baza]: {str(e)}")

    baza_id = callback_query.data.replace("baza_", "")
    await state.update_data(baza_id=baza_id)
    try:
        data = await state.get_data()
        fan_id = data['fan_id']
        questions = get_questions(fan_id=fan_id, baza_id=baza_id)
        
        if not questions:
            await bot.send_message(
                callback_query.from_user.id,
                "Boshqa bazadan yoki boshqa fandan savollar yechishga harakat qilib ko‘ring, bu xatolik adminga yuborildi!"
            )
            await bot.send_message(
                ADMIN,
                "Xatolik"
            )
            await state.finish()
            return
        await state.update_data(questions=questions, question_index=0, score=0)
        await send_next_question(callback_query.from_user.id, state)
    except Exception as e:
        await bot.send_message(
            callback_query.from_user.id,
            "Boshqa bazadan yoki boshqa fandan savollar yechishga harakat qilib ko‘ring, bu xatolik adminga yuborildi!1"
        )
        await bot.send_message(
            ADMIN,
            "Xatolik"
        )
        await state.finish()
    await bot.answer_callback_query(callback_query.id)

# Keyingi savolni yuborish
async def send_next_question(chat_id, state: FSMContext):
    data = await state.get_data()
    questions = data['questions']
    question_index = data['question_index']

    # Oldingi xabarlarni o‘chirish (rasm va matn)
    old_message_ids = data.get('message_ids', [])
    if old_message_ids:
        try:
            for message_id in old_message_ids:
                await bot.delete_message(chat_id, message_id)
        except Exception as e:
            print(f"Xabarlarni o‘chirishda xatolik[send next]: {str(e)}")

    if question_index >= len(questions):
            score = data['score']
            percentage = (score / 10) * 100

            try:
                # Fan nomini olish
                subjects = get_subjects()
                fan_name = next((f['name'] for f in subjects if int(f['id']) == int(data['fan_id'])), "Noma'lum fan")
                
                if fan_name == "Noma'lum fan":
                    print(f"Xatolik: Fan nomi topilmadi, fan_id: {data['fan_id']}")
                    # notify_admins(f"Fan nomi topilmadi: fan_id={data['fan_id']}")
            except Exception as e:
                fan_name = "Noma'lum fan"
                print(f"Xatolik fan nomini olishda: {str(e)}")
                # notify_admins(f"Fan nomi olish xatosi: {str(e)} - fan_id: {data['fan_id']}")

            try:
                # Baza nomini olish
                databases = get_databases()
                baza_name = next((b['name'] for b in databases if int(b['id']) == int(data['baza_id'])), "Noma'lum baza")

                if baza_name == "Noma'lum baza":
                    print(f"Xatolik: Baza nomi topilmadi, baza_id: {data['baza_id']}")
                    # notify_admins(f"Baza nomi topilmadi: baza_id={data['baza_id']}")
            except Exception as e:
                baza_name = "Noma'lum baza"
                print(f"Xatolik baza nomini olishda: {str(e)}")
                # notify_admins(f"Baza nomi olish xatosi: {str(e)} - baza_id: {data['baza_id']}")

            # Natijani chiqarish va saqlash
            try:
                result_message = (
                    f"🎉 *Quiz Natijalari*\n\n"
                    f"👤 *Ism:* {data.get('user_name')}\n"
                    f"📚 *Fan:* {fan_name}\n"
                    f"⚙️ *Baza:* {baza_name}\n"
                    f"⭐ *Natija:* {percentage:.0f} %"
                )
                await bot.send_message(
                    chat_id,
                    result_message,
                    parse_mode="Markdown",  # Markdown bilan formatlash
                    reply_markup=types.ReplyKeyboardRemove()
                )
                # save_result ni await bilan chaqirish
                await save_result(
                    telegram_id=chat_id,
                    baza_id=data['baza_id'],
                    fan_id=data['fan_id'],
                    natija=score,
                    ism=data.get('user_name')
                )
            except Exception as e:
                print(f"Natijani chiqarish yoki saqlashda xatolik: {str(e)}")
                # notify_admins(f"Natija xatosi: {str(e)} - chat_id: {chat_id}, score: {score}")
            await state.finish()
            return
    
    question = questions[question_index]
    options = question['javoblar']
    keyboard = get_options_keyboard(options)

    message_ids = []  # Yangi xabar ID’larini saqlash uchun ro‘yxat

    if question['image']:
        # Rasmni yuklash va yuborish
        image_url = question['image']
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()

            temp_dir = Path("/tmp")
            temp_file = temp_dir / f"temp_image_{chat_id}.png"

            with open(temp_file, 'wb') as f:
                f.write(response.content)

            with open(temp_file, 'rb') as photo:
                photo_message = await bot.send_photo(chat_id, photo=photo)
                message_ids.append(photo_message.message_id)
                text_message = await bot.send_message(
                    chat_id,
                    f"{question_index + 1}/10. {question['savol']}",
                    reply_markup=keyboard
                )
                message_ids.append(text_message.message_id)
            temp_file.unlink()
        except Exception as e:
            await bot.send_message(
                chat_id,
                "Rasmni yuklashda xatolik yuz berdi. Boshqa savolga o‘tamiz!",
                reply_markup=keyboard
            )
            notify_admins(f"Rasm yuklash xatosi: {str(e)} - URL: {image_url}")
            await state.update_data(question_index=question_index + 1)
            await send_next_question(chat_id, state)
    else:
        # Rasmsiz savolni yuborish
        message = await bot.send_message(
            chat_id,
            f"{question_index + 1}/10. {question['savol']}",
            reply_markup=keyboard
        )
        message_ids.append(message.message_id)

    # Yangi xabar ID’larini saqlash
    await state.update_data(message_ids=message_ids)
    await QuizState.answering.set()
    
# Javobni qayta ishlash
# Javobni qayta ishlash
async def process_answer(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    questions = data['questions']
    question_index = data['question_index']
    score = data['score']

    answer_index = int(callback_query.data.replace("answer_", ""))
    correct_answer = questions[question_index]['javob']
    user_answer = questions[question_index]['javoblar'][answer_index]

    # Oldingi xabarlarni o‘chirish (rasm va matn)
    message_ids = data.get('message_ids', [])
    if message_ids:
        try:
            for message_id in message_ids:
                await bot.delete_message(callback_query.from_user.id, message_id)
        except Exception as e:
            print(f"Xabarlarni o‘chirishda xatolik[process]: {str(e)}")

    # Kreativ notification
    if user_answer == correct_answer:
        score += 1
        await bot.answer_callback_query(
            callback_query.id,
            "✅ Ajoyib!",
            show_alert=True
        )
    else:
        await bot.answer_callback_query(
            callback_query.id,
            "❌ Afsus!",
            show_alert=True
        )

    await state.update_data(score=score, question_index=question_index + 1)
    await send_next_question(callback_query.from_user.id, state)

# Handlerlarni ro‘yxatdan o‘tkazish
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel_and_restart, text="🔙 Ortga Qaytish")
    dp.register_message_handler(quiz_button_handler, text="⚡ Quiz")
    dp.register_message_handler(cmd_quiz, commands=['quiz'])
    dp.register_callback_query_handler(process_fan, lambda c: c.data.startswith("fan_"), state=QuizState.choosing_fan)
    dp.register_callback_query_handler(process_baza, lambda c: c.data.startswith("baza_"), state=QuizState.choosing_baza)
    dp.register_callback_query_handler(process_answer, lambda c: c.data.startswith("answer_"), state=QuizState.answering)
    