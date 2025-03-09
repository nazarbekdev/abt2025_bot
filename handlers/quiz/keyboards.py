from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_quiz_keyboard():
    """Quiz tugmasi uchun klaviatura"""
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        KeyboardButton('Quiz')
    )

def get_fan_keyboard(fans):
    """Fanlar uchun inline tugmalar"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    for fan in fans:
        keyboard.insert(
            InlineKeyboardButton(text=fan['name'], callback_data=f"fan_{fan['id']}")
        )
    return keyboard

def get_baza_keyboard(bazas):
    """Bazalar uchun inline tugmalar"""
    keyboard = InlineKeyboardMarkup(row_width=1)
    for baza in bazas:
        keyboard.insert(
            InlineKeyboardButton(text=baza['name'], callback_data=f"baza_{baza['id']}")
        )
    return keyboard

def get_options_keyboard(options):
    """Savollar uchun 4 ta inline tugma (A, B, C, D)"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    for i, option in enumerate(options[:4]):  # Faqat 4 ta variant
        keyboard.insert(
            InlineKeyboardButton(text=option, callback_data=f"answer_{i}")
        )
    return keyboard