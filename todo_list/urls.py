from django.urls import path
from .views import main_page
from . import views

urlpatterns = [
    path('', main_page, name='main'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/category/<str:category_name>/', views.tasks_by_category, name='tasks_by_category'),
]