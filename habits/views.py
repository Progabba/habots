from rest_framework import generics, permissions
from .models import Habit
from .serializers import HabitSerializer

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    Класс для кастомной пагинации API ответов.

    Атрибуты:
        page_size (int): Количество элементов на одной странице по умолчанию.
        page_size_query_param (str): Параметр запроса для изменения количества элементов на странице.
        max_page_size (int): Максимальное количество элементов на странице.
    """

    page_size = 10  # Количество элементов на одной странице
    page_size_query_param = (
        "page_size"  # Позволяет менять размер страницы через параметр запроса
    )
    max_page_size = 50  # Максимальный размер страницы


class HabitListCreateView(generics.ListCreateAPIView):
    """
    Представление для получения списка и создания привычек пользователя.

    Разрешения:
        Только аутентифицированные пользователи имеют доступ к этому представлению.

    Пагинация:
        Использует кастомный класс пагинации `CustomPagination`.

    Методы:
        get_queryset: Фильтрует привычки, относящиеся только к текущему пользователю.
        list: Возвращает список привычек текущего пользователя с поддержкой пагинации.
    """

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PublicHabitListView(generics.ListAPIView):
    """
    Представление для получения списка публичных привычек.

    Доступ:
        Не требует аутентификации. Возвращает все привычки, отмеченные как публичные.

    Атрибуты:
        serializer_class: Сериализатор для представления данных привычек.
        queryset: Queryset, содержащий публичные привычки.
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(public=True)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для получения, обновления или удаления конкретной привычки.

    Разрешения:
        Только аутентифицированные пользователи имеют доступ к этому представлению.

    Методы:
        get_queryset: Фильтрует привычки, относящиеся только к текущему пользователю.
    """

    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)
