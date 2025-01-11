from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def fanlar_inline_keyboard():
    keyboard = InlineKeyboardMarkup()

    tar_ona_btn = InlineKeyboardButton("📖 Tarix - Ona tili va Adabiyot", callback_data="5-9")
    tar_ing_btn = InlineKeyboardButton("📘 Tarix - Ingliz tili", callback_data="5-11")
    tar_huq_btn = InlineKeyboardButton("⚖️ Tarix - Huquq", callback_data="5-12")
    tar_geo_btn = InlineKeyboardButton("🌍 Tarix - Geografiya", callback_data="5-10")
    huq_ing_btn = InlineKeyboardButton("📚 Huquq - Ingliz tili", callback_data="12-11")
    bio_ona_btn = InlineKeyboardButton("🔖 Biologiya - Ona tili va Adabiyot", callback_data="4-9")
    bio_kim_btn = InlineKeyboardButton("🧪 Biologiya - Kimyo", callback_data="4-8")
    kim_mat_btn = InlineKeyboardButton("📐 Kimyo - Matematika", callback_data="8-7")
    kim_bio_btn = InlineKeyboardButton("🧬 Kimyo - Biologiya", callback_data="8-4")
    ona_mat_btn = InlineKeyboardButton("📝 Ona tili va Adabiyot - Matematika", callback_data="9-7")
    ona_ing_btn = InlineKeyboardButton("📘 Ona tili va Adabiyot - Ingliz tili", callback_data="9-11")
    mat_fiz_btn = InlineKeyboardButton("📊 Matematika - Fizika", callback_data="7-6")
    mat_ing_btn = InlineKeyboardButton("💰 Matematika - Ingliz tili", callback_data="7-11")
    mat_geo_btn = InlineKeyboardButton("🌍 Matematika - Geografiya", callback_data="7-10")
    mat_ona_btn = InlineKeyboardButton("📖 Matematika - Ona tili va Adabiyot", callback_data="7-9")
    fiz_mat_btn = InlineKeyboardButton("⚛️ Fizika - Matematika", callback_data="6-7")
    fiz_ing_btn = InlineKeyboardButton("🛡️ Fizika - Ingliz tili", callback_data="6-11")
    ing_ona_btn = InlineKeyboardButton("📚 Ingliz tili - Ona tili va Adabiyot", callback_data="11-9")
    rus_tar_btn = InlineKeyboardButton("🇷🇺 Rus tili - Tarix", callback_data="13-5")
    rus_ing_btn = InlineKeyboardButton("📘 Rus tili - Ingliz tili", callback_data="13-11")
    rus_ona_btn = InlineKeyboardButton("📚 Rus tili - Ona tili va Adabiyot", callback_data="13-9")

    keyboard.row(mat_fiz_btn, mat_ona_btn)
    keyboard.row(mat_ing_btn, mat_geo_btn)
    keyboard.row(ona_ing_btn, ona_mat_btn)
    keyboard.row(fiz_mat_btn, fiz_ing_btn)
    keyboard.row(rus_tar_btn, rus_ing_btn)
    keyboard.row(rus_ona_btn, ing_ona_btn)
    keyboard.row(bio_ona_btn, bio_kim_btn)
    keyboard.row(kim_mat_btn, kim_bio_btn)
    keyboard.row(tar_ona_btn, tar_ing_btn)
    keyboard.row(tar_huq_btn, tar_geo_btn)
    keyboard.row(huq_ing_btn)

    return keyboard


def til_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data="1"),
        InlineKeyboardButton("🇷🇺 Rus tili", callback_data="2"),
    )
    return keyboard


def baza_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📚 Baza 1", callback_data="1"),
        InlineKeyboardButton("📘 Baza 2", callback_data="2"),
        InlineKeyboardButton("📕 Baza 3", callback_data="3"),
    )
    return keyboard


def tasdiqlash_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("✅ Tasdiqlash", callback_data="tasdiq"),
        InlineKeyboardButton("❌ Bekor qilish", callback_data="bekor"),
    )
    return keyboard
