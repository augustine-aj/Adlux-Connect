from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot, name='chat'),
    path('fetch_sidebar_data', views.fetch_sidebar_data, name='fetch_sidebar_data'),
    path('new_chat', views.new_chat_isPressed, name='new_chat'),
    path('get_chat_history', views.get_chat_history, name='get_chat_history'),
]