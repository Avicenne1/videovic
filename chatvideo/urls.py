from django.urls import path
from . import views

urlpatterns = [
    path('room/<str:room_name>/', views.room, name='room'),
    path('', views.lobby, name='video_lobby'),
]
