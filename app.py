from aiogram import executor
from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
import handlers
from handlers.block_test.avto_test_yuborish import scheduler, setup_scheduled_notifications  # Schedulerni import qilamiz


async def on_startup(dispatcher):
    # Birlamchi komandalarni o'rnatish (/start va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)

    # Schedulerni boshlash
    print("Scheduler ishga tushmoqda...")
    setup_scheduled_notifications()
    scheduler.start()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
