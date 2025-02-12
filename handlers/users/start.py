import os
import requests
import logging
import asyncio
from keyboards.button.main_kyb import main_keyboard  
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import CHANNEL
from keyboards.inline.subscriptions import check_button
from utils.misc import subscription

logging.basicConfig(level=logging.INFO)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    name = message.from_user.first_name
    args = message.get_args()

    url_post = os.getenv('CREATE_USER')
    url_get = os.getenv('USER_INFO')
    url_patch = os.getenv('USER_PATCH')

    referral_link = f"https://t.me/abt2025_bot?start={user_id}"

    try:
        check_user = requests.get(f'{url_get}{user_id}')
        if check_user.status_code == 200:
            await message.answer("Siz allaqachon ro'yxatdan o'tgansiz! 😊")
        else:
            inviter_id = int(args) if args and args.isdigit() else None

            data = {
                'name': name,
                'user_name': user_name,
                'telegram_id': user_id,
                'referral_link': referral_link,
            }

            if inviter_id:
                inviter_user = requests.get(f'{url_get}{inviter_id}')
                if inviter_user.status_code == 200:
                    inviter_data = inviter_user.json()
                    data['invited_by'] = inviter_data['id']

                    res = requests.post(url_post, data=data)
                    if res.status_code == 200:
                        balans = inviter_data.get('balans', 0) + 550
                        requests.patch(f'{url_patch}{inviter_id}', data={'balans': balans})
                        await bot.send_message(inviter_id, "⚡️ Sizga +550 so'm bonus berildi!")
                        await message.answer("Siz muvaffaqiyatli ro'yxatdan o'tdingiz!")
                else:
                    await message.answer("Taklif qiluvchi foydalanuvchi topilmadi.")
            else:
                res = requests.post(url_post, data=data)
                if res.status_code == 200:
                    await message.answer(f"Assalomu alaykum {message.from_user.first_name}!\n Siz muvaffaqiyatli ro'yxatdan o'tdingiz!")
                else:
                    await message.answer("Ro'yxatdan o'tishda xatolik yuz berdi.")

        check_sub_markup = InlineKeyboardMarkup()
        for channel in CHANNEL:
            try:
                chat = await bot.get_chat(channel)
                invite_link = await chat.export_invite_link()
                check_sub_markup.add(InlineKeyboardButton(
                    text=f"🧑‍🎓 {chat.title}",
                    url=invite_link
                ))
            except Exception as e:
                logging.error(f"Kanal uchun havola olishda xatolik: {channel} - {e}")

        check_sub_markup.add(InlineKeyboardButton(
            text="✅ Obunani tekshirish",
            callback_data="check_subs"
        ))

        await message.answer(
            "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:",
            reply_markup=check_sub_markup,
            disable_web_page_preview=True
        )

    except Exception as e:
        logging.exception("An error occurred: %s", str(e))


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    user_id = call.from_user.id  # `user_id` aniqlanmaganligi xatolik yuzaga keltiradi, shu sababli uni qo'shdik
    try:
        result = ""
        all_subscribed = True

        for channel in CHANNEL:
            status = await subscription.check(user_id=user_id, channel=channel)
            chat = await bot.get_chat(channel)
            invite_link = await chat.export_invite_link()

            if status:
                result += f"✅ <a href='{invite_link}'><b>{chat.title}</b></a> kanaliga obuna bo'lgansiz!\n\n"
            else:
                result += f"❌ <a href='{invite_link}'><b>{chat.title}</b></a> kanaliga obuna bo'lmagansiz! Obuna bo'lish uchun <a href='{invite_link}'>bu yerga bosing</a>.\n\n"
                all_subscribed = False

        if all_subscribed:
            success_msg = await call.message.answer(
                "Botdan to'liq foydalanishingiz mumkin!",
                reply_markup=main_keyboard()
            )
        else:
            await call.message.answer(result, disable_web_page_preview=True)

    except Exception as e:
        logging.exception("An error occurred in subscription check: %s", str(e))
