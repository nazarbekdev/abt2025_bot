from aiogram.types import Message
from loader import dp


@dp.message_handler(lambda message: message.text == "📖 Qo'llanma")
async def qollanma(message: Message):
    await message.answer(
        text="""<b>📚 BOTDAN FOYDALANISH BO‘YICHA QO‘LLANMA</b>

    ───────────────────────
    <b>✍️ Test Yechish Bo‘limi</b>

    🔹 <b>Test Buyurtma</b> — Yo‘nalishingizga mos testlarni buyurtma qilish imkoniyati.

    🔹 <b>Test Tekshirish</b> — Natijalarni aniqlash uchun 2 xil usul mavjud:
    • <b>Titul usuli</b> – natijalarni maxsus shtrix-kod orqali aniqlash.
    • <b>Oddiy usul</b> – an’anaviy usulda javoblaringizni tekshirish.
    Har bir foydalanuvchi o‘ziga mos usulni tanlash imkoniyatiga ega.

    🔹 <b>Test Tahlili</b> — Har bir testdan so‘ng sun’iy intellekt asosida tahlil qilish orqali natijalaringizni chuqur o‘rganish imkoniyati.

    🔹 <b>Savolda Xatolik</b> — Agar test savollarida xatolik aniqlasangiz, bu haqida xabar berishingiz mumkin.

    🔹 <b>Balans</b> — Hisobingiz haqida ma’lumot:
    • Har bir test narxi – <b>2900 so‘m</b>.
    • Hisobingizni to‘ldirish imkoniyati mavjud.

    🔹 <b>Do‘stlarni Taklif Qilish</b> — Do‘stlaringizni taklif qilib, <b>bonuslarga ega bo‘ling</b>!

    ───────────────────────
    <b>🧑‍🎓 Yo‘nalishlar</b>

    🔹 Fanlar majmuasini tanlang va siz uchun mavjud bo‘lgan yo‘nalishlarni ko‘ring.

    ───────────────────────
    <b>🏛️ Kvotalar</b>

    🔹 Fanlar majmuasini tanlang  
    🔹 Viloyatni tanlang  
    🔹 Oliygohni tanlang  
    Bu orqali sizga kerakli oliy ta’lim muassasasi kvotalari haqida ma’lumot olasiz.

    ───────────────────────
    <b>❓ Savol Yuborish</b>

    🔹 OTM haqida, kirish imtihonlari yoki oliy ta’lim muassasalari bo‘yicha savollaringizga javob olishingiz mumkin.

    ───────────────────────
    <b>📖 Qo‘llanma</b>

    🔹 Botdan foydalanish bo‘yicha to‘liq <b>yo‘riqnoma</b>.

    ───────────────────────
    <b>🛠️ Admin</b>

    🔹 <b>Dasturchi bilan bog‘lanish</b> uchun maxsus bo‘lim.
    Taklif va muammolaringizni admin orqali bildiring.

    ───────────────────────

    <i>Botdan samarali foydalaning va testlaringizda muvaffaqiyatga erishing! ✅ 😊</i>
    """,
        parse_mode="HTML"
    )

