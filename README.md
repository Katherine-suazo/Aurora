# Aurora

Proyecto de carga, listado y eliminación de archivos en Amazon S3.

## Seguridad

- `SEC-01`: `backend/.env` fuera del repo y `backend/.env.example` con placeholders.
- `SEC-02`: CORS restringido a `http://localhost:5173`.
- `SEC-03`: Validación de nombre, extensión y sanitización en backend.
- `SEC-04`: Validación de tamaño en frontend y backend.
- `SEC-05`: IAM mínimo privilegio a configurar en AWS para `ListBucket`, `GetObject`, `PutObject` y `DeleteObject`.
- `SEC-06`: Bucket privado con Block Public Access a configurar en AWS.
- `SEC-07`: Errores genéricos al cliente y logging interno en backend.
- `SEC-08`: Cifrado en reposo con SSE-S3 en backend y bucket.
- `SEC-09`: Ejecutar `pip-audit` y `npm audit` antes de entregar.
- `SEC-10`: Producción con HTTPS en frontend, backend y acceso a S3 mediante presigned URLs.

## Desarrollo

- Backend: `cd backend && python manage.py runserver`
- Frontend: `cd frontend/Auroraweb && npm run dev`

