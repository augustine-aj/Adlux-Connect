from django.urls import path, include
from . import views

urlpatterns =[
    path('', views.create_login, name='login'),
    path('signup/', views.create_signup, name='signup'),
    path('logout/', views.create_logout, name='logout')
]