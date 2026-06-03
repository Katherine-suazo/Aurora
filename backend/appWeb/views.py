#from django.shortcuts import render

from rest_framework import viewsets
from .models import Archivo
from .serializer import ArchivoSerializer

class ArchivoViewSet(viewsets.ModelViewSet):
    serializer_class = ArchivoSerializer
    queryset = Archivo.objects.all()

    
