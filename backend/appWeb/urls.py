from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import VerificacionEstado
from .views import UrlCarga
from .views import ArchivoS3List

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path("verificacion/", VerificacionEstado.as_view()),  # /api/verificacion
    path("upload/presigned-url", UrlCarga.as_view()),
    path("files/", ArchivoS3List.as_view()),    
]



