from django.urls import path

from . import views


app_name = 'chat'
urlpatterns = [
    path('c/lobby', views.lobby, name="lobby"),
    path('c/chat-redirect/<str:pk>', views.chat_redirect, name="redirect"),
    path('c/<str:uuid>', views.chat_room, name="room"),
]
