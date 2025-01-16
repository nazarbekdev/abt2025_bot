from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.chat.convert_message import ai_assistant
from keyboards.button.test_buyurtma_kyb import test_buyurtma_keyboard
from loader import dp, bot
import asyncio

# Test Tahlili uchun State yaratamiz
class TestTahliliState(StatesGroup):
    waiting_for_test = State()

test_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔚 Suhbatni tugatish")]
    ],
    resize_keyboard=True
)


@dp.message_handler(lambda message: message.text == "📊 Test Tahlili", state="*")
async def test_tahlili(message: Message, state: FSMContext):
    await message.answer(
        "Assalomu alaykum 😊\n"
        "Test natijalaringizni oldingizmi? Tahlil qilishga tayyor bo'lsangiz marhamat, "
        "sizga yordam berishdan xursandman 🤗\n\n📊 Natijalaringiz bilan xabar bering va boshlaymiz!",
        reply_markup=test_keyboard
    )
    await state.set_state(TestTahliliState.waiting_for_test)


@dp.message_handler(lambda message: message.text == "🔚 Suhbatni tugatish", state=TestTahliliState.waiting_for_test)
async def end_conversation(message: Message, state: FSMContext):
    await message.answer("✅ Suhbat tugatildi. Yana savollaringiz bo‘lsa, bemalol yozishingiz mumkin! 😊",
                         reply_markup=test_buyurtma_keyboard())
    await state.finish()  # State-ni tugatamiz


@dp.message_handler(state=TestTahliliState.waiting_for_test)
async def handle_test_analysis(message: Message, state: FSMContext):
    user_text = message.text
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # AI javobini olish
    response, input_token, output_token, total_token = ai_assistant(user_text)
    await asyncio.sleep(2)

    await message.answer(response)
