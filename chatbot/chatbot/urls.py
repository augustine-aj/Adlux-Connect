from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls'), name='chat'),
    path('', include('login.urls'), name='login')
]
