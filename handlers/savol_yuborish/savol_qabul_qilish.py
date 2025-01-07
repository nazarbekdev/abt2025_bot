import os
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loader import dp, bot
from dotenv import load_dotenv
from aiogram.dispatcher.filters.state import State, StatesGroup
load_dotenv()

ADMIN_ID = os.getenv('ADMINS')


class QuestionForm(StatesGroup):
    waiting_for_question = State()


@dp.message_handler(lambda message: message.text == "❓ Savol Yuborish")
async def ask_question(message: Message):
    await message.answer("✍️ Iltimos, savolingizni yozing:")
    await QuestionForm.waiting_for_question.set()


@dp.message_handler(state=QuestionForm.waiting_for_question)
async def send_question_to_admin(message: Message, state: FSMContext):
    if message.text:
        user_id = message.from_user.id
        user_name = message.from_user.username or "Ismi yo'q"
        question = message.text

        # Adminga xabar yuborish
        await bot.send_message(ADMIN_ID, f"📩 Yangi savol:\n\n👤 Foydalanuvchi: @{user_name}\n🆔 ID: {user_id}\n❓ Savol: {question}")

        # Foydalanuvchiga javob qaytarish
        await message.reply("✅ Savolingiz adminga yuborildi!")
    else:
        await message.reply("❌ Savolingizni tushunmadim, iltimos matn ko'rinishida yuboring.")
    await state.finish()
    