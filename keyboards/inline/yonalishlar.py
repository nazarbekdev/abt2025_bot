from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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


# Har bir sahifada nechta yo‘nalish ko‘rsatiladi
ITEMS_PER_PAGE = 10


# Sahifa tugmalarini generatsiya qiluvchi funksiya
def generate_keyboard(current_page: int = 0):
    keyboard = InlineKeyboardMarkup()

    # Sahifadagi yo‘nalishlarni ajratib olamiz
    start_index = current_page * ITEMS_PER_PAGE
    end_index = min(start_index + ITEMS_PER_PAGE, len(yonalishlar))  # Indexlarni cheklab qo‘yamiz
    page_items = list(yonalishlar.items())[start_index:end_index]

    # Debugging uchun loglar
    print(f"Current Page: {current_page}")
    print(f"Start Index: {start_index}, End Index: {end_index}")
    print(f"Items on this page: {page_items}")

    # Yo‘nalishlar tugmalari
    for name, id_ in page_items:
        keyboard.add(InlineKeyboardButton(text=name, callback_data=f"yonalish:{id_}:{name}"))

    # Pastki navigation tugmalari ("Oldingi" va "Keyingi")
    navigation_buttons = []
    if current_page > 0:  # Oldingi sahifa mavjudligini tekshiramiz
        navigation_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"page:{current_page - 1}"))
    if end_index < len(yonalishlar):  # Keyingi sahifa mavjudligini tekshiramiz
        navigation_buttons.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"page:{current_page + 1}"))

    if navigation_buttons:
        keyboard.row(*navigation_buttons)

    return keyboard

