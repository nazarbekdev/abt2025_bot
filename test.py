
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Bot tokeningizni kiriting
BOT_TOKEN = "7856412325:AAFTYx5Rp8fXjXosp1AEN_DR0gFUXIE6dX4"

# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Yo'nalishlar ro'yxati
yonalishlar = {
    'Tarix - Ona tili va adabiyoti': '1-2',
    'Biologiya - Ona tili va adabiyoti': '3-2',
    'Biologiya - Kimyo': '3-4',
    'Ona tili va adabiyoti - Matematika': '2-5',
    "Matematika - Ona tili va adabiyoti": '5-2',
    "Matematika - Geografiya": '5-6',
    "Matematika - Fizika": '5-7',
    "Kimyo - Matematika": '4-5',
    "Kimyo - Biologiya": '4-3',
    "Geografiya - Matematika": '6-5',
    'Ona tili va adabiyoti - Chet tili': '2-8',
    "O'zbek tili va adabiyoti - Chet tili": '9-8',
    'Rus tili va adabiyoti - Tarix': '10-1',
    "Qirg'iz tili va adabiyoti - Tarix": '11-1',
    "Qozoq tili va adabiyoti - Tarix": '12-1',
    "Qoraqalpoq tili va adabiyoti - Tarix": '13-1',
    "Turkman tili va adabiyoti - Tarix": '14-1',
    "Tojik tili va adabiyoti - Tarix": '15-1',
    "Ingliz tili - Ona tili va adabiyoti": '16-2',
    "Nemis tili - Ona tili va adabiyoti": '17-2',
    "Fransuz tili - Ona tili va adabiyoti": '18-2',
    "Tarix - Geografiya": '1-6',
    "Tarix - Chet tili": '1-8',
    "Tarix - Matematika": '1-5',
    "Huquqshunoslik fanlari - Chet tili": '19-8',
    "Fizika - Matematika": '7-5',
    'Rus tili va adabiyoti - Chet tili': '10-8',
    'Rus tili va adabiyoti - O\'zbek tili va adabiyoti': '10-9',
    'Chet tili - Ona tili va adabiyoti': '8-2',
    "Tojik tili va adabiyoti - Ona tili va adabiyoti": '15-2',
    "Turkman tili va adabiyoti - Ona tili va adabiyoti": '14-2',
    "Qozoq tili va adabiyoti - Ona tili va adabiyoti": '12-2',
    "Qoraqalpoq tili va adabiyoti - Ona tili va adabiyoti": '13-2',
    "Tarix - Kasbiy (ijodiy imtihon)": '1-20',
    "Kasbiy (ijodiy imtihon) - Ona tili va adabiyoti": '20-2',
    "Kasbiy (ijodiy imtihon) - Chet tili": '20-8',
    "Kasbiy (ijodiy imtihon) - Kasbiy (ijodiy imtihon)": '20-20'
}


# Yo'nalishlarni bo'laklarga ajratish
def get_direction_pages(items, page=1, per_page=10):
    start = (page - 1) * per_page
    end = start + per_page
    return list(items)[start:end]


# Yo'nalishlarni tugma qilish
def generate_keyboard(page=1):
    markup = InlineKeyboardMarkup(row_width=2)
    directions = get_direction_pages(yonalishlar.keys(), page=page)

    for i, direction in enumerate(directions, start=(page - 1) * 10 + 1):
        button = InlineKeyboardButton(text=f"{i}. {direction}", callback_data=f"dir_{i}")
        markup.add(button)

    # Oldingi va keyingi sahifalar tugmalari
    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"page_{page - 1}"))
    if len(get_direction_pages(yonalishlar.keys(), page=page + 1)) > 0:
        buttons.append(InlineKeyboardButton("Keyingi ➡️", callback_data=f"page_{page + 1}"))

    markup.row(*buttons)
    return markup


# Start komandasi
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Yo'nalishlardan birini tanlang:", reply_markup=generate_keyboard())


# Callback uchun handler
@dp.callback_query_handler(lambda c: c.data.startswith("page_"))
async def change_page(callback_query: types.CallbackQuery):
    page = int(callback_query.data.split("_")[1])
    await callback_query.message.edit_text("Yo'nalishlardan birini tanlang:", reply_markup=generate_keyboard(page=page))


# Yo'nalish ma'lumotini qaytarish
@dp.callback_query_handler(lambda c: c.data.startswith("dir_"))
async def show_direction(callback_query: types.CallbackQuery):
    direction_index = int(callback_query.data.split("_")[1]) - 1
    direction_name = list(yonalishlar.keys())[direction_index]
    direction_code = yonalishlar[direction_name]
    await callback_query.message.answer(f"Yo'nalish: {direction_name}\nKod: {direction_code}")


# Botni ishga tushirish
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
