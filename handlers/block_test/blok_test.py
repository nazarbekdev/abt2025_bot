from aiogram.types import Message
from loader import dp, bot
from keyboards.button.blok_test import blok_test_keyboard


@dp.message_handler(lambda msg: msg.text == "📋 Blok test")
async def blok_test(message: Message):
    await message.answer("<b>Blok testda qatnashish uchun ro'yxatdan o'ting!</b>\n\n"
                         "Har <b>Yakshanba</b> blok test yeching.\n"
                         "<b>Testlar bepul!</b> <i>(sinov doirasida bo'lgani uchun)</i>\n\n"
                         "🏆 Sovrinlar\n"
                         "🥇 1-o'rin: 50 000 so'm\n"
                         "🥈 2-o'rin: 30 000 so'm\n"
                         "🥉 3-o'rin: 10 000 so'm\n", parse_mode="HTML", reply_markup=blok_test_keyboard())
