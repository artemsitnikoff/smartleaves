"""
URL маршруты для API тегов
"""

from django.urls import path
from . import views
from apps.worksheets.views import WorksheetsByTagView

app_name = 'tags'

urlpatterns = [
    # Список всех тегов
    # GET /api/tags/
    path('', views.TagListView.as_view(), name='list'),

    # Популярные теги (топ-20)
    # GET /api/tags/popular/
    path('popular/', views.PopularTagsView.as_view(), name='popular'),

    # Worksheets по тегу с пагинацией
    # GET /api/tags/matematika/worksheets/
    path('<slug:tag_slug>/worksheets/', WorksheetsByTagView.as_view(), name='tag-worksheets'),

    # Детали тега
    # GET /api/tags/matematika/
    path('<slug:slug>/', views.TagDetailView.as_view(), name='detail'),
]
