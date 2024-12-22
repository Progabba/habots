from django.test import TestCase
from .models import Habit
from django.contrib.auth.models import User

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.habit = Habit.objects.create(
            user=self.user,
            action='Run',
            place='Park',
            time='07:00',
            duration=120
        )

    def test_habit_creation(self):
        self.assertEqual(self.habit.action, 'Run')
