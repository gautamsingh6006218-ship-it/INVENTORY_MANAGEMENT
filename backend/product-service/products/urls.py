from django.urls import path
from products import views

urlpatterns = [
    path('categories/', views.category_list, name='category-list'),
    path('electronics/', views.electronics_list, name='electronics-list'),
    path('food/', views.food_list, name='food-list'),
    path('clothing/', views.clothing_list, name='clothing-list'),

    path('categories/<int:pk>/', views.category_detail, name='category-detail'),
    path('electronics/<int:pk>/', views.electronics_detail, name='electronics-detail'),
    path('food/<int:pk>/', views.food_detail, name='food-detail'),
    path('clothing/<int:pk>/', views.clothing_detail, name='clothing-detail'),
]
