from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя, расширяющая стандартную модель AbstractUser.

    Поля:
        telegram_chat_id (CharField): Telegram Chat ID пользователя,
            используется для отправки уведомлений (необязательное поле).

    Методы:
        __str__: Возвращает строковое представление пользователя, отображающее его имя пользователя.
    """

    telegram_chat_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Telegram Chat ID для отправки уведомлений",
    )

    def __str__(self):
        return self.username
