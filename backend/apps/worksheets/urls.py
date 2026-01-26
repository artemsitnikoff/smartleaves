"""
URL маршруты для API рабочих листов
"""

from django.urls import path
from . import views

app_name = 'worksheets'

urlpatterns = [
    # Список всех рабочих листов (каталог) с пагинацией
    # GET /api/worksheets/
    path('', views.WorksheetListView.as_view(), name='list'),

    # Поиск с пагинацией
    # GET /api/worksheets/search/?q=математика
    path('search/', views.WorksheetSearchView.as_view(), name='search'),

    # Избранные для главной (без пагинации, фиксированное количество)
    # GET /api/worksheets/featured/
    path('featured/', views.FeaturedWorksheetsView.as_view(), name='featured'),

    # Скачивание PDF по ID
    # GET /api/worksheets/1/download/
    path('<int:pk>/download/', views.WorksheetDownloadView.as_view(), name='download'),

    # Детали worksheet по slug (карточка)
    # GET /api/worksheets/slozhenie-v-predelah-10/
    path('<slug:slug>/', views.WorksheetDetailView.as_view(), name='detail'),
]
