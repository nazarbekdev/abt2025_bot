from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def test_buyurtma_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    # Birinchi qator
    keyboard.add(KeyboardButton("📝 Test Buyurtma"), KeyboardButton("✅ Test Tekshirish"))

    # Ikkinchi qator
    keyboard.add(KeyboardButton("📊 Test Tahlili"), KeyboardButton("❓ Savolda Xatolik"))

    # Uchinchi qator
    keyboard.add(KeyboardButton("🔙 Ortga Qaytish"))

    return keyboard
