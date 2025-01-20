import re

def format_phone_number(phone_number):
    # Faqat raqamlarni olish uchun belgilarni tozalash
    digits = re.sub(r'\D', '', phone_number)

    # Raqam uzunligi tekshiriladi
    if len(digits) == 12 and digits.startswith("998"):
        # Namunadagi formatga keltirish
        formatted = f"+998 {digits[3:5]} {digits[5:8]} {digits[8:10]} {digits[10:]}"
    else:
        raise ValueError("Noto'g'ri telefon raqami formati")

    return formatted

# Test qilamiz
examples = [
    "998901234567",
    "+998 90 1234567",
    "+998901234567",
    "9989012 3 45 67"
]

for example in examples:
    try:
        print(format_phone_number(example))
    except ValueError as e:
        print(f"{example}: {e}")

