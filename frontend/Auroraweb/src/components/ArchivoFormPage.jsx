import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { getAllArchivos, crearArchivo, eliminarArchivo } from "../api/apiFile";
import { useNavigate, useParams } from "react-router-dom";
import { ArchivosList } from "../components/ArchivosLista";


export function ArchivoFormPage() {
    const { register, handleSubmit, formState:{errors}, setValue } = useForm();
    const navigate = useNavigate();
    const params = useParams();

    const onSubmit = handleSubmit(async (data) => {
        try {
            await crearArchivo(data);
            navigate('/files') // redireccionar
        }
        catch (error) {
            console.error('Error en onSubmit crearArchivo'.error)
        }
    })
}


return(

    <div>

        <form onSubmit={onSubmit}>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUlpload}>Subir archivo</button>
        </form>

    </div>

)
