from django.urls import path
from chat import views

urlpatterns = [
    path("chatroom/<int:pk>", views.chatroom, name = "chatroom"),
    path("ajax/<int:pk>/", views.ajax_load_messages, name="chatroom-ajax"),
    path("messageDelete/", views.messageDelete, name="messageDelete"),
    path("chatroombase/", views.chatroombase, name="chatroombase"),
]