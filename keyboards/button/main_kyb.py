from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    #Blok test
    keyboard.add(KeyboardButton("📋 Blok test"))

    # Birinchi qator
    keyboard.add(KeyboardButton("✍️ Test Yechish"), KeyboardButton("🧑‍🎓 Yo'nalishlar"))

    # Ikkinchi qator
    keyboard.add(KeyboardButton("🏛️ Kvotalar"), KeyboardButton("❓ Savol Yuborish"))

    # Uchinchi qator
    keyboard.add(KeyboardButton("📖 Qo'llanma"), KeyboardButton("🛠️ Admin"))

    return keyboard
