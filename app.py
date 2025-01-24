from aiogram import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from handlers.block_test.avto_test_yuborish import setup_scheduled_notifications
from handlers.block_test.testni_tekshirish import schedule_shifts

scheduler = AsyncIOScheduler()
scheduler.configure(timezone="Asia/Tashkent")


async def on_startup(dispatcher):
    # Birlamchi komandalarni o'rnatish (/start va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)

    # Schedulerni boshlash
    setup_scheduled_notifications(scheduler)  # avto test yuborish
    schedule_shifts(scheduler)  # test holatini tekshirish
    scheduler.start()  # schedule ga run berish


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
