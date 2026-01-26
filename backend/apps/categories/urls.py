"""
URL маршруты для API категорий
"""

from django.urls import path
from . import views
from apps.worksheets.views import WorksheetsByCategoryView

app_name = 'categories'

urlpatterns = [
    # Список всех категорий (плоский)
    # GET /api/categories/
    path('', views.CategoryListView.as_view(), name='list'),

    # Дерево категорий (для меню)
    # GET /api/categories/tree/
    path('tree/', views.CategoryTreeView.as_view(), name='tree'),

    # Worksheets по категории с пагинацией
    # GET /api/categories/matematika/worksheets/
    path('<slug:category_slug>/worksheets/', WorksheetsByCategoryView.as_view(), name='category-worksheets'),

    # Детали категории
    # GET /api/categories/matematika/
    path('<slug:slug>/', views.CategoryDetailView.as_view(), name='detail'),
]
