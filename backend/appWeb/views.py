from rest_framework import viewsets
from .models import Archivo
from .serializer import ArchivoSerializer

from rest_framework.views import APIView
from rest_framework.response import Response


# este es para el crud
class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = Archivo.objects.all().order_by("-fecha_subida")
    serializer_class = ArchivoSerializer

# este para los endpoint
class VerificacionEstado(APIView):
    def get(self, request):
        return Response({ "satus": "ok" })
    
# ...
class UrlCarga(APIView):
    def post(self, request):
        return Response({ "visitarURL":"https://aws-hola.com", "key":"uploads/archivo.doxc" }) #