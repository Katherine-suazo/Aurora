from rest_framework import serializers
#from .models import Archivo


#class ArchivoSerializer(serializers.ModelSerializer):
#   class Meta:
#        model = Archivo
""" #        fields = '__all__'


class s3ArchivoSerializer(serializers.Serializer):
    filename = serializers.CharField()
    file_url = serializers.URLField()
    size = serializers.IntegerField() """