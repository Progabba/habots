from celery import shared_task

from config.settings import TELEGRAM_BOT_TOKEN
from .models import Habit
import requests

BOT_TOKEN = TELEGRAM_BOT_TOKEN

@shared_task
def send_reminder(habit_id):
    try:
        # Получаем привычку
        habit = Habit.objects.get(id=habit_id)

        # Проверяем, есть ли Telegram Chat ID у пользователя
        if not habit.user.telegram_chat_id:
            print(f"User {habit.user.username} does not have a Telegram Chat ID.")
            return

        # Формируем текст уведомления
        message = (
            f"Напоминание о вашей привычке:\n\n"
            f"Действие: {habit.action}\n"
            f"Место: {habit.place}\n"
            f"Время: {habit.time.strftime('%H:%M')}\n"
            f"Награда: {habit.reward or 'нет'}\n"
        )
        params = {
            'text': message,
            'chat_id': habit.user.telegram_chat_id,
        }


        # Отправляем сообщение через Telegram
        response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', params=params)

    except Habit.DoesNotExist:
        print(f"Habit with id {habit_id} does not exist.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


