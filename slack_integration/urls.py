from django.urls import path
from . import views

urlpatterns = [
    path('command', views.command, name='command'),
]
