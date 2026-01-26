"""
Пагинация для API списков рабочих листов
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class WorksheetPagination(PageNumberPagination):
    """
    Пагинатор для списка рабочих листов

    Параметры запроса:
    - page: номер страницы (по умолчанию 1)
    - page_size: количество элементов на странице (по умолчанию 21, максимум 100)

    Примеры использования:
    - /api/worksheets/ -> первая страница, 21 элементов
    - /api/worksheets/?page=2 -> вторая страница
    - /api/worksheets/?page=1&page_size=30 -> первая страница, 30 элементов
    """

    # Количество элементов на странице по умолчанию (делится на 3 для красивого отображения)
    page_size = 21

    # Параметр для изменения количества элементов
    page_size_query_param = 'page_size'

    # Максимальное количество элементов на странице
    max_page_size = 100

    # Название параметра для номера страницы
    page_query_param = 'page'

    def get_paginated_response(self, data):
        """
        Кастомный формат ответа с пагинацией

        Возвращает:
        {
            "count": 156,                  // общее количество элементов
            "total_pages": 8,              // общее количество страниц
            "current_page": 1,             // текущая страница
            "page_size": 20,               // элементов на странице
            "next": "http://.../2",        // URL следующей страницы (или null)
            "previous": null,              // URL предыдущей страницы (или null)
            "results": [...]               // массив с данными
        }
        """
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page_size,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
