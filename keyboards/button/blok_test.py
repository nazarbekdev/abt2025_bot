from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def blok_test_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    # Birinchi qator
    keyboard.add(KeyboardButton("📋 Ro'yxatdan o'tish"), KeyboardButton("📝 Testni tekshirish"))

    # Ikkinchi qator
    keyboard.add(KeyboardButton("🔙 Ortga Qaytish"))

    return keyboard
