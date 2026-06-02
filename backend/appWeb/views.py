#from django.shortcuts import render

from rest_framework import viewsets
from .models import SubirArchivo
from .serializer import SubirArchivoSerializer

class SubirArchivoViewSet(viewsets.ModelViewSet):
    serializer_class = SubirArchivoSerializer
    queryset = SubirArchivo.objects.all()

    
