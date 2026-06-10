from django.db import models


class Archivo(models.Model):
    nombre = models.CharField(max_length=255)
    key = models.CharField(max_length=500)
    tamaño = models.BigIntegerField()
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
