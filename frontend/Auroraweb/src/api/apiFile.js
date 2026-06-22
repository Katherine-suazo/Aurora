import axios from 'axios';

const ApiFile = axios.create({
    baseURL: "http://localhost:8000/api", // donde corre django
});


//--------------------------------------------------------------------------- S3

// GET
export const obtenerListaArchivos = async () => {
    try {
        const response = await ApiFile.get('/files/');
        console.log(response);
        return response.data;
    }
    catch (error) {
        console.error("Error en get archivos:", error);
        return [];
    }
};

// DELETE
export const EliminarArchivo = async (key) => {
    try {
        const keyUrl = key.split('/').map(encodeURIComponent).join('/');
        const response = await ApiFile.delete(`/files/${keyUrl}/`)
        console.log(response);
        return response.data;
    }
    catch (error) {
        console.error("Error en delete archivos:", error);
        return [];
    }
}

// POST
export const obtenerUrl = async (documento) => {
    try {
        const response = await ApiFile.post('/upload/presigned-url', {
            nombre: documento.name,
            size: documento.size,
            type: documento.type,
        });
        console.log(response);
        return response.data;
    }
    catch (error) {
        console.error("Error en post archivos:", error);
        return null;
    }
};


// PUT
export const subirArchivos = async (url, documento, headers = {}) => {
    try {
        const response = await axios.put(url, documento, {
            headers: {
                'Content-Type': documento.type || 'application/octet-stream',
                ...headers,
            }
        });
        console.log(response);
        return response;   
    }
    catch (error) {
        console.error("Error en put archivos:", error);
        return null;
    }
};


//----------------------------------------------------------------------------- DYNAMODB


// POST
export const guardarMetadataArchivo = async ({ key, documento }) => {
    try {
        const response = await ApiFile.post('/upload/metadata', {
            key,
            nombre_proyecto: documento.name,
            tamano: documento.size,
        });
        console.log(response);
        return response.data;
    }
    catch (error) {
        console.error("Error guardando metadata:", error);
        return null;
    }
};

