import { useState } from "react";
import { useForm } from "react-hook-form";
import { obtenerUrl, subirArchivos} from "../api/apiFile";
import { useNavigate, useParams } from "react-router-dom";
import { ArchivosList } from "./ArchivosLista";
import "../style/Estilo.css";


const extensionesPermitidas = [ "docx", "pptx" ];
const maxSize = 18 * 1024 * 1024;

export function ArchivoForm() {
    const [archivo, setArchivo] = useState(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const extension = file.name.split(".").pop().toLowerCase();
        if (!extensionesPermitidas.includes(extension)) {
            alert("Solo docx y pptx");
            return;
        }

        if (file.size > maxSize) {
            alert("El archivo supera el limite de 18 MB");
            return;
        } 

        setArchivo(file)
    };

    const handleUpload = async () => {
        if (!archivo) {
            alert("Selecciona un archivo antes de subir");
            return;
        }

        const responseUrl = await obtenerUrl(archivo);
        console.log(responseUrl);
        await subirArchivos(responseUrl, archivo);
        //llamar api
        //obyener visitarurl
        //llamar api 2 con visitarurl
        //si esto es status 200 ok
        console.log("archivo seleccionado", archivo);
    };


    return (
        <div className="container">

            <h2>Subir archivo</h2>

            <input type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Subir archivo</button>
            
        </div>
    );

}
