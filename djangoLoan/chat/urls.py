from django.urls import path
from . import views

urlpatterns = [
    path('room/<int:room_id>/', views.chat_room, name='chat_room'),
]