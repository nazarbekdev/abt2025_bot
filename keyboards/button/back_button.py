from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def back_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    keyboard.add(KeyboardButton("🔙 Ortga Qaytish"))

    return keyboard
