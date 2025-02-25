from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_room, name='chat_room'),
    path('api/messages/', views.message_list, name='message_list'),
    path('api/send/', views.send_message, name='send_message'),
    path('send/', views.send_message, name='send_message'),
]