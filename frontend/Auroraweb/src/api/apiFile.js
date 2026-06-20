import axios from 'axios';

const ApiFile = axios.create({
    baseURL: "http://localhost:8000/api", // donde corre django
});

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

export const obtenerUrl = async (documento) => {
    try {
        const response = await ApiFile.post('/upload/presigned-url', {nombre:documento.name});
        console.log(response);
        return response.data.visitarURL;
    }
    catch (error) {
        console.error("Error en get archivos:", error);
        return [];
    }
};

export const subirArchivos = async (url, documento) => {
    try {
        const response = await axios.put(url, documento, {
            headers: {
                'Content-Type': documento.type || 'application/octet-stream'
            }
        });
        console.log(response);
        
        return response.data;
    }
    catch (error) {
        console.error("Error en get archivos:", error);
        return [];
    }
};
