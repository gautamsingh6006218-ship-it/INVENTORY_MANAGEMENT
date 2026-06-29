from django.urls import path
from . import views

urlpatterns = [
    path('suppliers/', views.supplier_list, name='supplier-list'),                            # GET all / POST create
    path('suppliers/<int:pk>/', views.supplier_detail, name='supplier-detail'),               # GET one / PUT update / DELETE remove
    path('suppliers/<int:pk>/toggle-active/', views.toggle_active, name='supplier-toggle-active'),  # PATCH activate/deactivate
]
