from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def tekshirish_usullari():
    keyboard = InlineKeyboardMarkup()

    titul_btn = InlineKeyboardButton("Titul", callback_data="titul")
    oddiy_btn = InlineKeyboardButton("Oddiy", callback_data="oddiy")

    keyboard.row(titul_btn, oddiy_btn)

    return keyboard
