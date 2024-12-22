from celery import shared_task
from .models import Habit

@shared_task
def send_reminder(habit_id):
    habit = Habit.objects.get(id=habit_id)
    # Логика отправки уведомления через Telegram
