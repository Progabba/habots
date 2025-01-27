from django.test import TestCase
# from .models import Habit
# from django.contrib.auth.models import User


class HabitModelTest(TestCase):
    """
    Тесты для модели Habit.
    """
    pass
    # def setUp(self):
    #     """
    #     Устанавливает начальные данные для тестов.
    #
    #     Создаётся тестовый пользователь и привычка, связанная с этим пользователем.
    #     """
    #     self.user = User.objects.create_user(username="testuser", password="password")
    #     self.habit = Habit.objects.create(
    #         user=self.user,
    #         action="Run",
    #         place="Park",
    #         time="07:00",
    #         duration=120,
    #     )
    #
    # def test_habit_creation(self):
    #     """
    #     Проверяет, что привычка создаётся с правильными данными.
    #     """
    #     self.assertEqual(self.habit.action, "Run")
    #     self.assertEqual(self.habit.place, "Park")
    #     self.assertEqual(self.habit.time.strftime("%H:%M"), "07:00")
    #     self.assertEqual(self.habit.duration, 120)
    #     self.assertEqual(self.habit.user, self.user)
    #
    # def test_habit_str_method(self):
    #     """
    #     Проверяет, что метод __str__ модели Habit возвращает корректное строковое представление.
    #     """
    #     self.assertEqual(str(self.habit), "Run")
