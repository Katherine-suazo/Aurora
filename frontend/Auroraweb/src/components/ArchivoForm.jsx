import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { getAllArchivos, crearArchivo, eliminarArchivo } from "../api/apiFile";
import { useNavigate, useParams } from "react-router-dom";
import { ArchivosList } from "./ArchivosLista";


export function ArchivoForm() {
    const [archivo, setArchivo] = useState(null);

    const handleFileChange = (e) => {
        setArchivo(e.target.files[0]);
    };
    const handleUpload = () => {
        console.log("archivo seleccionado", archivo);
    };

    return (
        <div>

            <h2>Subir archivo</h2>

            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Subir archivo</button>

            {archivo && (
                <div>
                    <p>Nombre: {archivo.name}</p>
                    <p>Tamaño: {(archivo.size / 1024 / 1024).toFixed(2)} MB </p>
                </div>
            )}

        </div>
    );

}


