from django.urls import path
from . import views

urlpatterns = [
    # GET all notifications / POST create new notification
    path('notifications/', views.notification_list, name='notification-list'),
    # GET single notification / DELETE by ID
    path('notifications/<int:pk>/', views.notification_detail, name='notification-detail'),
    # PATCH mark notification as read or unread
    path('notifications/<int:pk>/mark-read/', views.mark_read, name='mark-read'),
]