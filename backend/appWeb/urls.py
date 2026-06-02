from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubirArchivoViewSet

router = DefaultRouter()
router.register(r'', SubirArchivoViewSet, basename='subir')

urlpatterns = [
    path('', include(router.urls)),
]


# todo este codigo genera por defecto el CRUD
