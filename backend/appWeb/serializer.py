from rest_fraemework import serializers
from .models import SubirArchivo


class SubirArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubirArchivo
        fields = '__all__'