import requests
from dotenv import load_dotenv
import os

# .env dan admin ID sini olish
load_dotenv()
ADMINS = os.getenv('ADMINS', '').split(',')

API_URL = 'http://127.0.0.1:8000/api/quiz/v1/'

def get_subjects():
    """Fanlar ro‘yxatini olish"""
    response = requests.get(f"{API_URL}subjects/")
    response.raise_for_status()
    return response.json()

def get_databases():
    """Bazalar ro‘yxatini olish"""
    response = requests.get(f"{API_URL}database-types/")
    response.raise_for_status()
    return response.json()

def get_questions(fan_id, baza_id):
    """Fan va baza bo‘yicha 10 ta savol olish"""
    response = requests.get(f"{API_URL}questions/{fan_id}/{baza_id}/")
    response.raise_for_status()
    return response.json()

async def save_result(telegram_id, baza_id, fan_id, natija, ism):
    """Natijani saqlash (mavjud bo‘lsa PATCH, yo‘q bo‘lsa POST)"""
    # Mavjud natijani tekshirish
    response = requests.get(
        f"{API_URL}results/?telegram_id={telegram_id}&baza={baza_id}&fan={fan_id}"
    )
    response.raise_for_status()
    results = response.json()

    if results and len(results) > 0:
        # PATCH bilan yangilash
        quiz_user_id = results[0]['id']
        response = requests.patch(
            f"{API_URL}results/{quiz_user_id}/",
            json={'natija': natija, 'urinishlar': results[0]['urinishlar'] + 1}
        )
    else:
        # POST bilan yangi yaratish
        response = requests.post(
            f"{API_URL}results/",
            json={
                'ism': ism,
                'telegram_id': telegram_id,
                'baza': baza_id,
                'fan': fan_id,
                'natija': natija,
                'urinishlar': 1
            }
        )
    response.raise_for_status()
    return response.json()

def notify_admins(error_message):
    """Adminga xatolik haqida xabar yuborish"""
    for admin_id in ADMINS:
        requests.post(
            f"{API_URL}send_bot/",  # Sizning xabar yuborish endpoint’ingiz
            json={'chat_id': admin_id, 'text': error_message}
        ).raise_for_status()
