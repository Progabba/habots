from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        if data['pleasant_habit']:
            if data.get('reward') or data.get('related_habit'):
                raise serializers.ValidationError('Pleasant habits cannot have rewards or related habits.')
        if data['duration'] > 120:
            raise serializers.ValidationError('Duration cannot exceed 120 seconds.')
        if data['frequency'] < 1:
            raise serializers.ValidationError('Frequency must be at least once per week.')
        return data
