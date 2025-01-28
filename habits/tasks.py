from celery import shared_task
from config.settings import TELEGRAM_BOT_TOKEN
from .models import Habit
import requests
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

BOT_TOKEN = TELEGRAM_BOT_TOKEN


@shared_task
def send_reminder(habit_id):
    """
    Отправляет напоминание о привычке пользователю в Telegram.

    Параметры:
        habit_id (int): ID привычки, для которой отправляется напоминание.

    Логика:
        - Получает привычку из базы данных по переданному ID.
        - Проверяет, указан ли Telegram Chat ID у пользователя.
        - Формирует текст уведомления, включающий действие, место, время и награду.
        - Отправляет сообщение через Telegram API.

    Исключения:
        - Habit.DoesNotExist: Если привычка с указанным ID не найдена.
        - Все остальные исключения логируются.
    """
    try:
        # Получаем привычку
        habit = Habit.objects.get(id=habit_id)

        # Проверяем, есть ли Telegram Chat ID у пользователя
        if not habit.user.telegram_chat_id:
            logger.warning(
                f"Пользователь {habit.user.username} не указал Telegram Chat ID."
            )
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
            "text": message,
            "chat_id": habit.user.telegram_chat_id,
        }

        # Отправляем сообщение через Telegram
        response = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params=params
        )

        # Проверяем статус ответа
        if response.status_code == 200:
            logger.info(
                f"Уведомление успешно отправлено для пользователя {habit.user.username}."
            )
        else:
            logger.error(
                f"Ошибка при отправке уведомления для пользователя {habit.user.username}: {response.status_code}, {response.text}"
            )

    except Habit.DoesNotExist:
        logger.error(f"Привычка с id {habit_id} не найдена.")
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
