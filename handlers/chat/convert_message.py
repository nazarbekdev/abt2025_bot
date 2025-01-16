import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY")
)


def ai_assistant(message):
    completion = client.chat.completions.create(
        model="gpt-4o",
        store=True,
        messages=[
            {"role": "system",
             "content": "Siz o‘qituvchisiz va faqat ilmiy hamda ijobiy savollarga javob berasiz,"
                        " haqoratli so'zlar ishlatmang, samimiy bo'ling, foydalanuvchilar abituriyentlardir,"
                        " ular senga test tahlili va tushunmagan savollarga javob olish uchun so'rov yuborishadi:"
                        " savollar soni 90 ta, majburiy fanlar: (1-30) 1.1 balldan, fan1: (31-60) 3.1 balldan, "
                        "fan2: (61-90) 2.1 balldan, umumiy 189 ball. Abituriyent fan nomlari bilan natijalarni "
                        "berishi mumkin, majburiy fandan: {son} deb yuborsagina majburiydan natijasi deb qabul qil,"
                        " qolgan fan1 va fan2 larga fan nomi va nechta topgani haqida yozib "
                        "jo'natadi(masalan: tarix: 24, geografiya: 18), ularni topgan natijasiga qarab "
                        "boshidan feedbacklar ber va qiynalgan savollarini qisqacha izoh bilan tushuntirishini so'ra "
                        "va imkon qadar qisqa va lo'nda javob ber! Nomaqbul yoki noqonuniy mavzularga javob bermang."
                        "Har bir javob berganingdan so'ng,xabar pastiga bir qator tashab © 2024 TestifyHub deb xabar ham ber"},
            {"role": "user", "content": f"{message}"}
        ]
    )

    answer = completion.choices[0].message.content
    input_token = completion.usage.completion_tokens
    output_token = completion.usage.prompt_tokens
    total_token = completion.usage.total_tokens

    return answer, input_token, output_token, total_token
