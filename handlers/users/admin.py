from aiogram.types import Message
from loader import dp


@dp.message_handler(lambda message: message.text == "🛠️ Admin")
async def admin(message: Message):
    await message.answer(
        "🧑‍💻 <b>TestifyHub loyihasining muallifi: Mr Nazarbek</b>\n\n"
        "👨‍💻 Dasturchi: @mr_uzdev\n"
        "💡 <b>Yangi g'oyalar, xatolar yoki takliflar bo'lsa, bemalol yozing!</b>\n\n"
        "🔥 <b>Admin haqida:</b>\n"
        "— Kunduzi kod yozadi 💻\n"
        "— Kechasi esa g'oyalarni sinovdan o'tkazadi 🌙\n"
        "— Qahva bilan yashaydi ☕\n"
        "— Har qanday muammoni yechadi! 🔧\n\n"
        "📡 <b>Yangi imkoniyatlar va yangilanishlar doimo nazoratda!</b>\n\n"
        "🚀 <i><b>Bizni tanlaganingiz uchun tashakkur!</b></i>",
        parse_mode="HTML"
    )

