from django.urls import path
from orders import views

urlpatterns = [
    path('', views.order_list, name='order-list'),
    path('<int:pk>/', views.order_detail, name='order-detail'),
    path('<int:pk>/status/', views.update_status, name='order-status'),
]
