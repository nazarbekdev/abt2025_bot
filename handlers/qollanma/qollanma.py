from aiogram.types import Message
from loader import dp

text = """
    BOTDAN FOYDALANISH BO'YICHA QO'LLANMA

• ✍️ Test Yechish

📝 Test Buyurtma — yo'nalishingizga mos test buyurtma berish

✅ Test Tekshirish — natijalarni aniqlash, 2 ta usul orqali aniqlash imkoniyati taqdim etilgan: Titul va Oddiy usul. har bir foydalanuvchi o'ziga mos usul orqali tekshirish imkoniyati mavjud

📊 Test Tahlili — suniy intellekt asosida tahlil qilish orqali har bir testdan so'ng o'zingizni tahlil qilish imkoniyatini taqdim etadi

❓ Savolda Xatolik — taqdim etilgan test savollarida xatolik mavjud bo'lsa bu haqida xabar berish

💰 Balans — sizning hisobingiz, har bir test 2900 so'mdan tashkil qilinadi, bu yerda hisobingiz haqida ma'lumot va to'ldirish imkoniyati

🤝 Do'stlarni Taklif Qilish — do'stlaringizni taklif qilish orali bonuslarga ega bo'ling


• 🧑‍🎓 Yo'nalishlar

- Fanlar majmuasini tanlang va siz uchun qanday yo'nalishlar bor ekanligini ko'rishingiz mumkin


• 🏛️ Kvotalar 

- Fanlar majmuasini tanlang
- Viloyatni tanlang
- Oliygohni tanlang


• ❓ Savol Yuborish

- OTM haqida, kirish imtihonlari haqida ma'lumot olish uchun savol bering


• 📖 Qo'llanma

- Botdan foydalanish yuzasidan yo'riqnoma


• 🛠️ Admin

- Dasturchi bilan bog'lanish
"""


@dp.message_handler(lambda message: message.text == "📖 Qo'llanma")
async def qollanma(message: Message):
    await message.answer(text)
