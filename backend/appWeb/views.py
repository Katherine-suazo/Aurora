# views.py
import uuid
import boto3
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Archivo
from .serializer import ArchivoSerializer


# Este es para el crud estándar (Listar, Guardar en BD, Eliminar, etc.)
class ArchivoViewSet(viewsets.ModelViewSet):
    queryset = Archivo.objects.all().order_by("-fecha_subida")
    serializer_class = ArchivoSerializer


# Este para verificar que el backend responda correctamente
class VerificacionEstado(APIView):
    def get(self, request):
        return Response({ "status": "ok" })
    

# Este genera la URL firmada real conectándose a AWS S3
class UrlCarga(APIView):
    def post(self, request):
        nombre_original = request.data.get('nombre')
        
        # Validación básica por si el front no envía el nombre del archivo
        if not nombre_original:
            return Response(
                {"error": "El campo 'nombre' es obligatorio para generar la URL."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 1. Generar una Key única para que los archivos no se pisen en el S3
        ext = nombre_original.split('.')[-1]
        unique_id = uuid.uuid4().hex
        s3_key = f"uploads/{unique_id}.{ext}" # Conservamos tu estructura de carpetas 'uploads/'
        
        try:
            # 2. Inicializar el cliente de AWS Boto3 con las credenciales del .env
            # Recuerda que AWS_SESSION_TOKEN es vital por los créditos institucionales
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                aws_session_token=settings.AWS_SESSION_TOKEN,
                region_name=settings.AWS_S3_REGION_NAME
            )
            
            # 3. Solicitar a AWS la URL firmada para una operación de subida (put_object)
            url_firmada = s3_client.generate_presigned_url(
                ClientMethod='put_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': s3_key,
                },
                ExpiresIn=3600 # La URL será válida por 1 hora
            )
            
            # 4. Responder al frontend con la estructura que necesitas
            return Response({ 
                "visitarURL": url_firmada, 
                "key": s3_key 
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Error al conectar con AWS: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )