from django.urls import path
from . import views

urlpatterns = [
    # GET all stock entries / POST create new stock entry
    path('', views.inventory_list, name='inventory-list'),

    # GET / PUT / DELETE a single stock entry by ID
    path('<int:pk>/', views.inventory_detail, name='inventory-detail'),

    # PUT increase stock quantity — used when new stock arrives in warehouse
    path('<int:pk>/add-stock/', views.add_stock, name='add-stock'),

    # PUT decrease stock quantity — used when an order is placed
    path('<int:pk>/reduce-stock/', views.reduce_stock, name='reduce-stock'),
]