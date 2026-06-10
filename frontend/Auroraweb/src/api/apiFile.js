import axios from 'axios';

const ApiFile = axios.create({
    baseURL: "http://localhost:8000/api", // donde corre django
});


// GET
export const getAllArchivos = async () => {
    try {
        const response = await ApiFile.get('/files/');
        return response.data;
    }
    catch (error) {
        console.error("Error en get archivos:", error);
        return [];
    }
};

// POST
export const crearArchivo = async (archivoData) => {
    try {
        const response = await ApiFile.post('/files/', archivoData);
        return response;
    }
    catch (error) {
        console.error("Error en post archivo:", error);
        return null;
    }
}

// DELETE
export const eliminarArchivo = async (archivoId) => {
    try {
        const response = await ApiFile.delete(`files/${archivoId}/`);
        return response;
    }
    catch (error) {
        console.error("Error en delete archivo:", error);
        return null;
    }
}
