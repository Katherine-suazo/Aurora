import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { getAllArchivos, crearArchivo, eliminarArchivo } from "../api/apiFile";
import { useNavigate, useParams } from "react-router-dom";


export function ArchivoFormPage() {
    const { register, handleSubmit, formState:{errors}, setValue } = useForm();
    const navigate = useNavigate();
    const params = useParams();

    const onSubmit = handleSubmit(async (data) => {
        await crearArchivo(data);
        navigate('/files') // redireccionar
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
