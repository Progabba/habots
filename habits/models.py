from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings  # Для использования AUTH_USER_MODEL


class Habit(models.Model):
    """
        Модель для хранения информации о привычках пользователей.

        Поля:
            user (ForeignKey): Ссылка на пользователя, владеющего привычкой.
            action (CharField): Название действия, описывающее привычку.
            place (CharField): Место, где выполняется привычка.
            time (TimeField): Время выполнения привычки.
            reward (CharField): Награда за выполнение привычки (необязательное поле).
            pleasant_habit (BooleanField): Указывает, является ли привычка приятной (по умолчанию False).
            related_habit (ForeignKey): Ссылка на связанную привычку, если такая имеется
                (может быть NULL или пустым).
            frequency (IntegerField): Частота выполнения привычки (количество раз в неделю, по умолчанию 1).
            public (BooleanField): Указывает, является ли привычка публичной (по умолчанию False).
            duration (IntegerField): Длительность выполнения привычки в секундах (по умолчанию 120).

        Методы:
            __str__: Возвращает строковое представление привычки, отображающее её действие.
        """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")
    action = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    reward = models.CharField(max_length=255, null=True, blank=True)
    pleasant_habit = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_to",
    )
    frequency = models.IntegerField(default=1)  # Количество раз в неделю
    public = models.BooleanField(default=False)
    duration = models.IntegerField(default=120)  # Время выполнения в секундах

    def clean(self):
        """
        Проверяет корректность данных для связанной и приятной привычки.
        """
        if self.pleasant_habit:
            if self.reward:
                raise ValidationError("Приятная привычка не может иметь вознаграждение.")
            if self.related_habit:
                raise ValidationError("Приятная привычка не может быть связана с другой привычкой.")
        if self.related_habit and not self.related_habit.pleasant_habit:
            raise ValidationError("Связанная привычка должна быть с признаком 'приятная'.")

    def save(self, *args, **kwargs):
        self.clean()  # Вызов проверки перед сохранением
        super().save(*args, **kwargs)

    def __str__(self):
        return self.action
