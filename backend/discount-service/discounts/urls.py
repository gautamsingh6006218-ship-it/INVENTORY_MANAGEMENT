from django.urls import path
from . import views

urlpatterns = [
    path('discounts/', views.discount_list, name='discount-list'),
    path('discounts/<int:pk>/', views.discount_detail, name='discount-detail'),
    path('discounts/<int:pk>/toggle-active/', views.toggle_active, name='discount-toggle-active'),
]