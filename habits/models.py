from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    action = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    time = models.TimeField()
    reward = models.CharField(max_length=255, null=True, blank=True)
    pleasant_habit = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='related_to'
    )
    frequency = models.IntegerField(default=1)  # Количество раз в неделю
    public = models.BooleanField(default=False)
    duration = models.IntegerField(default=120)  # Время выполнения в секундах

    def __str__(self):
        return self.action
