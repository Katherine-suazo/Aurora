# views.py
import uuid
import boto3
from botocore.config import Config
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse

from .models import Archivo

# Este es para el crud estándar (Listar, Guardar en BD, Eliminar, etc.)
class ArchivoS3List(APIView):
    def get(self, request, format=None):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN,
            region_name=settings.AWS_S3_REGION_NAME,
            config=Config(signature_version='s3v4')
        )
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        
        try:
            response = s3_client.list_objects_v2(Bucket=bucket_name)
            archivos_data = []
            print(response['Contents'])
            if 'Contents' in response:
                for obj in response['Contents']:
                    archivos_data.append({
                        'nombre': obj['Key'],
                        'tamano_bytes': obj['Size'],
                        'ultima_modificacion': obj['LastModified']
                    })

            return Response({'archivos': archivos_data}, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
                region_name=settings.AWS_S3_REGION_NAME,
                config=Config(signature_version='s3v4')
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
