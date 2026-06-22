from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import VerificacionEstado
from .views import UrlCarga
from .views import ArchivoS3List
from .views import EliminarArchivoS3
from .views import ArchivoMetadata

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls) ),
    path( "verificacion/", VerificacionEstado.as_view() ),
    path( "upload/presigned-url", UrlCarga.as_view() ),
    path( "upload/metadata", ArchivoMetadata.as_view() ),
    path( "files/", ArchivoS3List.as_view() ),  
    path( "files/<path:key>/", EliminarArchivoS3.as_view() ),  
]


