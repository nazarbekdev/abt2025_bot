import os
import requests
from loader import dp, bot
import logging
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.config import CHANNEL
from keyboards.inline.subscriptions import check_button
from utils.misc import subscription
from keyboards.button.main_kyb import main_keyboard
logging.basicConfig(level=logging.INFO)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user_id = message.from_user.id
        user_name = message.from_user.username
        name = message.from_user.first_name
        args = message.get_args()

        # Userni ro'yxatga olish
        url_post = os.getenv('CREATE_USER')
        url_get = os.getenv('USER_INFO')
        check_user = requests.get(f'{url_get}{user_id}')

        # Referal  yaratish
        referral_link = f"https://t.me/abt2025_bot?start={user_id}"

        if args:
            inviter_id = int(args)
            # Bazaga kim taklif qilganini yozib qo'yamiz
            # Bu yerda Django ORM kodini ishlating

            await message.answer(f"Sizni foydalanuvchi {inviter_id} taklif qildi!")


        if check_user.status_code != 200:
            res = requests.post(url_post, data={'name': name, 'user_name': user_name, 'telegram_id': user_id, 'referral_link': referral_link})
            if res.status_code == 200:
                logging.info("User ro'yxatga olindi: %s", res.json())

        # Kanallarga obuna bo'lishni talab qilish
        channels_format = ""
        for channel in CHANNEL:
            chat = await bot.get_chat(channel)
            invite_link = await chat.export_invite_link()
            channels_format += f"✅ <a href='{invite_link}'>{chat.title}</a>\n"

        await message.answer(
            f"Assalomu alaykum, {message.from_user.full_name}!\nBotdan foydalanish uchun, quyidagi kanallarga obuna bo'ling:\n\n{channels_format}\n\nSizning referalingiz: {referral_link}",
            reply_markup=check_button,
            disable_web_page_preview=True
        )

    except Exception as e:
        logging.exception("An error occurred: %s", str(e))


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    try:
        result = ""
        all_subscribed = True
        for channel in CHANNEL:
            status = await subscription.check(user_id=call.from_user.id, channel=channel)
            chat = await bot.get_chat(channel)
            invite_link = await chat.export_invite_link()

            if status:
                result += f"✅ <a href='{invite_link}'><b>{chat.title}</b></a> kanaliga obuna bo'lgansiz!\n\n"
            else:
                result += f"❌ <a href='{invite_link}'><b>{chat.title}</b></a> kanaliga obuna bo'lmagansiz! Obuna bo'lish uchun <a href='{invite_link}'>bu yerga bosing</a>.\n\n"
                all_subscribed = False

        if all_subscribed:
            # Foydalanuvchi uchun asosiy klaviatura
            await call.message.answer(
                "Rahmat! Siz barcha kanallarga obuna bo'lgansiz. Botdan to'liq foydalanishingiz mumkin.",
                reply_markup=main_keyboard()
            )
        else:
            await call.message.answer(result, disable_web_page_preview=True)
    except Exception as e:
        logging.exception("An error occurred in subscription check: %s", str(e))
