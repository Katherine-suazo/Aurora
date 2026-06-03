import axios from 'axios';

const ApiFile = axios.create({
    baseURL: "http://localhost:8080/api",
});


// GET
export const getAllArchivos = async () => {
    try {
        const response = await ApiFile.get('/files');
        return response;
    }
    catch (error) {
        console.error("Error en get archivos:", error);
        return null;
    }
};

// POST
export const crearArchivo = async (fileData) => {
    try {
        const response = await ApiFile.post('/upload/presigned-url', fileData);
        return response;
    }
    catch (error) {
        console.error("Error en post archivo:", error);
        return null;
    }
}

// DELETE
export const eliminarArchivo = async (fileId) => {
    try {
        const response = await ApiFile.delete(`files/${fileId}/`);
        return response;
    }
    catch (error) {
        console.error("Error en delete archivo:", error);
        return null;
    }
}
