from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def taklif_qilish(referal_link):
    keyboard = InlineKeyboardMarkup()

    share_button = InlineKeyboardButton(
        text="📎 Do'stlarni taklif qilish",
        url=f"https://t.me/share/url?url={referal_link}&text=🔥 Do'stlaringizni taklif qiling va bonusga ega bo'ling!"
    )
    keyboard.add(share_button)

    return keyboard
