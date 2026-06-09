import { useState, useEffectse } from "react";
import { useForm } from "react-hook-form";
import { getAllArchivos, crearArchivo, eliminarArchivo } from "../api/apiFile";
import { useNavigate, useParams } from "react-router-dom";
import { ArchivosList } from "./ArchivosLista";
import "../style/Estilo.css";


export function ArchivoForm() {
    const [archivo, setArchivo] = useState(null);
    const formData = new FormData();

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        setArchivo(file)
    };

    const handleUpload = () => {
        console.log("archivo seleccionado", archivo);
    };

    formData.append("archivo", archivo);

    return (
        <div className="container">

            <h2>Subir archivo</h2>

            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Subir archivo</button>

            <h2>Lista de archivos</h2>

            {archivo ? (
                <ArchivosList archivo={archivo} />
            ) : (
                <p>no hay archivos subidos aun</p>
            )}
            

        </div>
    );

}
