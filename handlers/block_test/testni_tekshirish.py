import ast
import os
import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from loader import dp


class FormTekshir(StatesGroup):
    check = State()


@dp.message_handler(lambda message: message.text == "📝 Testni tekshirish")
async def tekshirish_(message: Message):
    await message.answer("❗️ Javoblarni ushbu formatda jo'nating 👇")
    await message.answer("1234567*abcdabcdab...cd")
    await FormTekshir.check.set()  # Holatni o'rnatamiz


# Faqat "tekshirish" holatida kelgan xabarlarni ushlash
@dp.message_handler(state=FormTekshir.check)
async def tekshirish_(message: Message, state: FSMContext):
    user_msg_ = message.text

    if '*' not in user_msg_:
        await message.answer("Iltimos, namunadagidek formatda jo'nating!!!")
        return

    book_id, user_keys = user_msg_.split('*')
    user_keys = user_keys.upper()

    if len(book_id) != 7:
        await message.answer('Kitob ID 7 xonadan iborat bo\'lishi kerak!')
        await state.finish()
        return

    if len(user_keys) != 90:
        await message.answer('Javoblar kaliti 90 tadan iborat bo\'lishi kerak!')
        await state.finish()
        return

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
            correct_answer = key[str(i)]
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
        summary = (f"\nKitob ID: {book_id}\n\n"
                   f"Majburiy fanlar: {mandatory_correct} ta\n"
                   f"Fan1: {fan1_correct} ta\n"
                   f"Fan2: {fan2_correct} ta\n\n"
                   f"Umumiy ball: {total_score:.1f}")

        result_output = "\n".join(result) + "\n\n" + summary
        await start_.delete()
        await message.answer(result_output)
    else:
        await message.answer('Bunday kitobcha mavjud emas!')
    await state.finish()