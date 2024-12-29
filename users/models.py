from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    telegram_chat_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Telegram Chat ID для отправки уведомлений"
    )

    def __str__(self):
        return self.username