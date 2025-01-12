from aiogram.types import Message
from loader import dp, bot
from keyboards.inline.dostlarni_taklif_qilish import taklif_qilish


@dp.message_handler(lambda message: message.text == "🤝 Do'stlarni Taklif Qilish")
async def dostlarni_taklif_qilish(message: Message):
    referal_link = f"https://t.me/abt2025_bot?start={message.from_user.id}"

    await message.answer("""
🔥 💰 BONUS OLISH IMKONIYATI! 🔥

Do'stlaringizni taklif qiling va har bir tashrif buyurgan do'stingiz uchun 550 so'm bonus yutib oling! 💵
✨ Sizning yutug‘ingiz cheklanmagan – qancha ko‘p taklif qilsangiz, shuncha ko‘p bonus yig‘asiz! 🚀
🎯 Do'stlarni taklif qilish uchun ushbu referal havolani ulashing va bonuslaringizni yig‘ishni boshlang!   
    """, reply_markup=taklif_qilish(referal_link))
