from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.report_list, name='report-list'),
    path('reports/<int:pk>/', views.report_detail, name='report-detail'),
]
