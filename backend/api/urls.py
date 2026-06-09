from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # no hay
    path('api/', include('appWeb.urls')), # cuando ejecutemos django >> http://127.0.0.1:8000/api/
]
