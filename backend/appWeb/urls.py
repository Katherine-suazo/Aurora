from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ArchivoViewSet
from .views import VerificacionEstado
from .views import UrlCarga

router = DefaultRouter()
router.register(r'files', ArchivoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("verificacion/", VerificacionEstado.as_view()),  # /api/verificacion
    path("upload/presigned-url", UrlCarga.as_view()),   
]



