from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    #Blok test
    keyboard.add(KeyboardButton("📋 Blok test"), KeyboardButton("⚡ Quiz"))
    

    # Birinchi qator
    keyboard.add(KeyboardButton("✍️ Test Yechish"), KeyboardButton("❓ Savol Yuborish"))
    # Quiz test
    # keyboard.add(KeyboardButton("⚡ Quiz"))
    # Ikkinchi qator
    keyboard.add(KeyboardButton("🏛️ Kvotalar"), KeyboardButton("🧑‍🎓 Yo'nalishlar"))

    # Uchinchi qator
    keyboard.add(KeyboardButton("💰 Balans"), KeyboardButton("🤝 Do'stlarni Taklif Qilish"))

    # To'rtinchi qator
    keyboard.add(KeyboardButton("📖 Qo'llanma"), KeyboardButton("🛠️ Admin"))

    return keyboard
