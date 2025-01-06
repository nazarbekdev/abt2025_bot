from aiogram.types import Message
from loader import dp, bot


@dp.message_handler(lambda message: message.text == "❓ Savolda Xatolik")
async def savolda_xatolik(message: Message):
    await message.answer(
        "Sizga yuborilgan test savollarida xatolik bor bo'lsa, iltimos, ushbu savolni"
        " rasmga(screenshot) olib adminlarimizga yuboring!\n\n"
        "Admin: @abt2025_admin")
