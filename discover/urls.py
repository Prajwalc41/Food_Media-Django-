from django.urls import path
from . import views

urlpatterns = [
    path('discover/', views.discover, name='discover'),
    path('food-history/<int:pk>/', views.food_history_detail, name='food_history_detail'),
]
