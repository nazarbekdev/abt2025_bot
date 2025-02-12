import ast
import os
import requests
from datetime import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from apscheduler.triggers.cron import CronTrigger
from keyboards.button.blok_test import blok_test_keyboard
from keyboards.button.test_tekshir_ortga_qaytish import ortga_qaytish
from loader import dp, bot


class FormTekshir(StatesGroup):
    check = State()


# Vaqt intervallarida ekanligini tekshirish
def is_within_interval(test_time, start, end):
    if start <= test_time <= end:
        return True
    return False


@dp.message_handler(lambda message: message.text == "📝 Testni tekshirish")
async def check_sheet(message: Message):
    await message.answer(f'<b>Sizning telegram ID:</b> {message.from_user.id}\n\n<b>🔗 Test tekshirish uchun havola 👇</b>\nhttps://testifyhub-uz-test-tekshirish.netlify.app', parse_mode='HTML')

@dp.message_handler(lambda message: message.text == "📝 Testni")
async def tekshirish_(message: Message):
    user_id = message.from_user.id
    url = os.getenv('BLOK_TEST_GET')
    req = requests.get(f"{url}{user_id}")

    today = datetime.today().strftime('%d.%m.%Y')
    hour = datetime.now().strftime('%H:%M')
    date_object = datetime.strptime(today, "%d.%m.%Y")
    converted_date = date_object.strftime("%d.%m.%y")  # 01.01.2025 --> 01.01.25

    if req.status_code == 200:
        date_ = req.json()['rejalashtirilgan_vaqt'].split('⏰')[0].strip()[2:]
        start_time = req.json()['rejalashtirilgan_vaqt'].split('⏰')[1].strip().split(' - ')[0]
        end_time = req.json()['rejalashtirilgan_vaqt'].split('⏰')[1].strip().split(' - ')[1]

        status = {
            'kutmoqda': '🟡 Kutmoqda',
            'yechmoqda': '🟠 Yechmoqda',
            'yakunlandi': '🟢 Yakunlandi',
            'topshirmadi': '🔴 Topshirmadi'
        }

        test_status = status[req.json()['status']]

        if converted_date == date_ and test_status != '🟢 Yakunlandi':
            if is_within_interval(hour, start_time, end_time):
                await message.answer("❗️ Javoblarni ushbu formatda jo'nating 👇")
                await message.answer("1234567*abcdabcdab...cd", reply_markup=ortga_qaytish())
                await FormTekshir.check.set()
            else:
                await message.answer("🔒 Test tekshirish imkoni mavjud emas!\n"
                                     f"📌 Vaqt intervali mos kelmadi, so'nggi blok "
                                     f"testingizni <b>{date_} | {start_time} - {end_time}</b> uchun rejalashtirgansiz!\n\n"
                                     f"Test holati: {test_status}",
                                     parse_mode="HTML")
        else:
            await message.answer(f"Test holati: {test_status}\n\n"
                                 f"⚙️ Texnik muammo bo'lgan bo'lsa adminga murojaat qiling: @abt2025_admin",
                                 parse_mode='HTML')
    else:
        print('Req error: ', req.status_code)


# Faqat "tekshirish" holatida kelgan xabarlarni ushlash
@dp.message_handler(state=FormTekshir.check)
async def tekshirish_(message: Message, state: FSMContext):
    user_msg_ = message.text
    if user_msg_ == '🔙 Ortga Qaytish':
        await state.finish()
        await message.answer("Blok test bo'limidasiz", reply_markup=blok_test_keyboard())

    elif '*' not in user_msg_:
        await message.answer("Iltimos, namunadagidek formatda jo'nating!!!")

    book_id, user_keys = user_msg_.split('*')
    user_keys = user_keys.upper()
    book_id_status, user_keys_status = False, False
    if len(book_id) != 7:
        await message.answer('Kitob ID 7 xonadan iborat bo\'lishi kerak!')
    else:
        book_id_status = True

    if len(user_keys) != 90:
        await message.answer('Javoblar kaliti 90 tadan iborat bo\'lishi kerak!')
    else:
        user_keys_status = True

    if book_id_status and user_keys_status:
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
        user_id = message.from_user.id

        # Natijalarni saqlash uchun foydalanuvchini ma'lumotlarini olish
        url = os.getenv('BLOK_TEST_GET')
        req = requests.get(f"{url}{user_id}")

        ism = req.json()['ism_familiya']
        fan1 = req.json()['fan1']
        fan2 = req.json()['fan2']
        viloyat = req.json()['viloyat']

        data = {
            'telegram_id': user_id,
            'ism': ism,
            'viloyat': viloyat,
            'blok1': fan1,
            'blok2': fan2,
            'majburiy': mandatory_correct,
            'fan1': fan1_correct,
            'fan2': fan2_correct,
            'ball': total_score,
            'javoblari': user_msg_
        }

        # Natijalarni saqlash
        url_res = os.getenv('NATIJALAR_POST')
        r = requests.post(url_res, data)

        if r.status_code == 200:
            # Foydalanuvchini statusini yangilash
            url_status = os.getenv('BLOK_TEST_PATCH')
            r_status = requests.patch(f"{url_status}{user_id}", data={'status': 'yakunlandi'})
            await start_.delete()
            await message.answer(result_output)
            await state.finish()
        else:
            await start_.delete()
            await message.answer(str(r.status_code))
    else:
        await message.answer('Bunday kitobcha mavjud emas!')
        await state.finish()


# Foydalanuvchini tekshirish va natijalarni qayta ishlash
async def handle_user_test(user, current_shift):
    try:
        scheduled_time = datetime.strptime(user['rejalashtirilgan_vaqt'].split('⏰')[1].strip().split(' - ')[1], "%H:%M").time()
        current_time = datetime.strptime(current_shift, "%H:%M").time()
        if current_time == scheduled_time:
            if user['status'] == 'yechmoqda':
                url_patch = os.getenv('BLOK_TEST_PATCH')
                r = requests.patch(f"{url_patch}{user['telegram_id']}", data={'status': 'topshirmadi'})
                await bot.send_message(chat_id=user['telegram_id'], text="Hurmatli foydalanuvchi test yakunlandi, "
                                                                         "javoblaringizni yubormadingiz!\n\n"
                                                                         "Test holati: 🔴 Topshirmadi")
                data = {
                    'telegram_id': user['telegram_id'],
                    'ism': user['ism_familiya'],
                    'viloyat': user['viloyat'],
                    'blok1': user['fan1'],
                    'blok2': user['fan2'],
                    'majburiy': 0,
                    'fan1': 0,
                    'fan2': 0,
                    'ball': 0.0,
                    'javoblari': '-'
                }

                # Natijalarni saqlash
                url_res = os.getenv('NATIJALAR_POST')
                r = requests.post(url_res, data)
            else:
                await bot.send_message(chat_id=user['telegram_id'], text="🏁 Test yakunlandi")

        else:
            print()
    except Exception as e:
        print()


# API orqali barcha foydalanuvchilarni tekshirish
async def check_user_test_results(current_shift):
    try:
        url_user_all = os.getenv('BLOK_TEST_ALL')
        response = requests.get(url_user_all)
        response.raise_for_status()
        users = response.json()

        for user in users:
            await handle_user_test(user, current_shift)
    except Exception as e:
        print(f"API ma'lumotlarini olishda xatolik: {e}")


# Har bir smenani rejalashtirish
def schedule_shifts(scheduler):
    for shift in ["11:00", "13:00", "17:00", "21:00", "23:00"]:
        hour, minute = map(int, shift.split(":"))
        scheduler.add_job(
            check_user_test_results, CronTrigger(hour=hour, minute=minute), args=[shift]
        )
