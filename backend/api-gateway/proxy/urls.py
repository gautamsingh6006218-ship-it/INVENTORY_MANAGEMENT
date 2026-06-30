from django.urls import path
from . import views

urlpatterns = [
    path('<str:service>/<path:path>', views.forward, name='forward'),
    path('<str:service>/', views.forward, name='forward'),
]