import uuid
import logging
import os
import boto3
from botocore.config import Config
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from urllib.parse import unquote
# from .models import Archivo

logger = logging.getLogger(__name__)


def extraer_nombre_original_archivo(nombre):
    nombre_archivo = str(nombre).replace("\\", "/").split("/")[-1].strip()
    return nombre_archivo or None


def extension_permitida(nombre_archivo):
    extensiones_permitidas = {".docx", ".pptx"}
    _, extension = os.path.splitext(nombre_archivo)
    return extension.lower() in extensiones_permitidas


def tamanio_permitido(size, max_size):
    try:
        return int(size) <= max_size
    except (TypeError, ValueError):
        return False


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
            if 'Contents' in response:
                for obj in response['Contents']:
                    archivos_data.append({
                        'nombre': obj['Key'],
                        'tamano_bytes': obj['Size'],
                        'ultima_modificacion': obj['LastModified']
                    })

            return Response({'archivos': archivos_data}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("Error al listar archivos desde S3")
            return Response({'error': 'No se pudo obtener la lista de archivos.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Este para verificar que el backend responda correctamente
class VerificacionEstado(APIView):
    def get(self, request):
        return Response({ "status": "ok" })
    

# Este genera la URL firmada real conectándose a AWS S3
class UrlCarga(APIView):
    def post(self, request):
        nombre_original = request.data.get('nombre')
        size = request.data.get("size")
        max_file_size = 18 * 1024 * 1024

        if not nombre_original:
            return Response(
                {"error": "El campo 'nombre' es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        nombre_archivo = extraer_nombre_original_archivo(nombre_original)
        if not nombre_archivo:
            return Response(
                {"error": "El nombre del archivo no es válido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not extension_permitida(nombre_archivo):
            return Response(
                {"error": "Extension no permitida."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if size is None:
            return Response(
                {"error": "El tamaño del archivo es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not tamanio_permitido(size, max_file_size):
            return Response(
                {"error": "El archivo supera el tamaño permitido."},
                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            )

        unique_id = uuid.uuid4().hex[:8]
        s3_key = f"uploads/{unique_id}-{nombre_archivo}"

        try:
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
                    'ServerSideEncryption': 'AES256',
                },
                ExpiresIn=3600 # La URL será válida por 1 hora
            )

            return Response({ 
                "visitarURL": url_firmada, 
                "key": s3_key 
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("Error al generar presigned URL")
            return Response({"error": "No se pudo generar la URL de carga."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class EliminarArchivoS3(APIView):
    def delete(self, request, key):
        key = unquote(key).strip()

        if not key:
            return Response({"error": "La key del archivo es obligatoria."}, status=status.HTTP_400_BAD_REQUEST)

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
            s3_client.delete_object(Bucket=bucket_name, Key=key)
            return Response( {"mensaje": f"Archivo '{key}' eliminado correctamente de S3"}, status=status.HTTP_200_OK )

        except Exception as e:
            logger.exception("Error al eliminar archivo en S3")
            return Response({ "error": "No se pudo eliminar el archivo." }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
