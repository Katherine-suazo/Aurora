import uuid
import logging
import os
import boto3 # nos permite interactuar con aws services
from boto3.dynamodb.conditions import Attr
from botocore.config import Config
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
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
    

#------------------------------------------------------------------------------------------- dynamoDB

def obtener_tabla_dynamodb():
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        aws_session_token=settings.AWS_SESSION_TOKEN,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    return dynamodb.Table(settings.DYNAMODB_TABLE_NAME)


def guardar_metadata_dynamodb(nombre_proyecto, s3_key, tamano):
    table = obtener_tabla_dynamodb()
    item = {
        'id_tabla': uuid.uuid4().hex,
        'nombre_proyecto': nombre_proyecto,
        's3_key': s3_key,
        'url_archivo': f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{s3_key}",
        'fecha_subida': timezone.now().isoformat(),
        'tamano': int(tamano),
    }
    table.put_item(Item=item)
    return item


def eliminar_metadata_dynamodb_por_s3_key(s3_key):
    table = obtener_tabla_dynamodb()
    response = table.scan( FilterExpression=Attr('s3_key').eq(s3_key) )
    items = response.get('Items', [])

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            FilterExpression=Attr('s3_key').eq(s3_key),
            ExclusiveStartKey=response['LastEvaluatedKey'],
        )
        items.extend(response.get('Items', []))

    key_names = [key['AttributeName'] for key in table.key_schema]
    for item in items:
        table.delete_item( Key={key_name: item[key_name] for key_name in key_names} )

    return len(items)

# ------------------------------------------------------------------------------------------ S3

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
            print(e)
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
                "key": s3_key,
                "headers": {
                    "x-amz-server-side-encryption": "AES256",
                },
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception("Error al generar presigned URL")
            return Response({"error": "No se pudo generar la URL de carga."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ArchivoMetadata(APIView):
    def post(self, request):
        key = request.data.get('key')
        nombre_proyecto = request.data.get('nombre_proyecto')
        tamano = request.data.get('tamano')

        if not key:
            return Response({"error": "La key del archivo es obligatoria."}, status=status.HTTP_400_BAD_REQUEST)

        if not nombre_proyecto:
            return Response({"error": "El nombre del proyecto es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        if not tamanio_permitido(tamano, 18 * 1024 * 1024):
            return Response({"error": "El tamaño del archivo no es válido."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            item = guardar_metadata_dynamodb(nombre_proyecto, key, tamano)
            return Response({"metadata": item}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception("Error al guardar metadata en DynamoDB")
            return Response({"error": "No se pudo guardar la metadata del archivo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
            metadata_eliminada = eliminar_metadata_dynamodb_por_s3_key(key)
            return Response(
                {
                    "mensaje": f"Archivo '{key}' eliminado correctamente.",
                    "metadata_eliminada": metadata_eliminada,
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.exception("Error al eliminar archivo")
            return Response({ "error": "No se pudo eliminar el archivo." }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
