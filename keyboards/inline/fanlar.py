from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def fanlar_inline_keyboard():
    keyboard = InlineKeyboardMarkup()

    tar_ona_btn = InlineKeyboardButton("📖 Tarix - Ona tili va Adabiyot", callback_data="tarix_ona")
    tar_ing_btn = InlineKeyboardButton("📘 Tarix - Ingliz tili", callback_data="tar_ing")
    tar_huq_btn = InlineKeyboardButton("⚖️ Tarix - Huquq", callback_data="tar_huq")
    tar_geo_btn = InlineKeyboardButton("🌍 Tarix - Geografiya", callback_data="tar_geo")
    huq_ing_btn = InlineKeyboardButton("📚 Huquq - Ingliz tili", callback_data="huq_ing")
    bio_ona_btn = InlineKeyboardButton("🔖 Biologiya - Ona tili va Adabiyot", callback_data="bio_ona")
    bio_kim_btn = InlineKeyboardButton("🧪 Biologiya - Kimyo", callback_data="bio_kim")
    kim_mat_btn = InlineKeyboardButton("📐 Kimyo - Matematika", callback_data="kim_mat")
    kim_bio_btn = InlineKeyboardButton("🧬 Kimyo - Biologiya", callback_data="kim_bio")
    ona_mat_btn = InlineKeyboardButton("📝 Ona tili va Adabiyot - Matematika", callback_data="ona_mat")
    ona_ing_btn = InlineKeyboardButton("📘 Ona tili va Adabiyot - Ingliz tili", callback_data='ona_ing')
    mat_fiz_btn = InlineKeyboardButton("📊 Matematika - Fizika", callback_data="mat_fiz")
    mat_ing_btn = InlineKeyboardButton("💰 Matematika - Ingliz tili", callback_data="mat_ing")
    mat_geo_btn = InlineKeyboardButton("🌍 Matematika - Geografiya", callback_data="mat_geo")
    mat_ona_btn = InlineKeyboardButton("📖 Matematika - Ona tili va Adabiyot", callback_data="mat_ona")
    fiz_mat_btn = InlineKeyboardButton("⚛️ Fizika - Matematika", callback_data="fiz_mat")
    fiz_ing_btn = InlineKeyboardButton("🛡️ Fizika - Ingliz tili", callback_data="fiz_ing")
    ing_ona_btn = InlineKeyboardButton("📚 Ingliz tili - Ona tili va Adabiyot", callback_data="ing_ona")
    rus_tar_btn = InlineKeyboardButton("🇷🇺 Rus tili - Tarix", callback_data="rus_tar")
    rus_ing_btn = InlineKeyboardButton("📘 Rus tili - Ingliz tili", callback_data="rus_ing")
    rus_ona_btn = InlineKeyboardButton("📚 Rus tili - Ona tili va Adabiyot", callback_data="rus_ona")

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
