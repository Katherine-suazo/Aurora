import { useState } from "react";
import { guardarMetadataArchivo, obtenerUrl, subirArchivos} from "../api/apiFile";
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

        const datosCarga = await obtenerUrl(archivo);
        if (!datosCarga?.visitarURL || !datosCarga?.key) {
            alert("No se pudo generar la URL de subida");
            return;
        }
        console.log(datosCarga.visitarURL);

        const uploadResponse = await subirArchivos(datosCarga.visitarURL, archivo, datosCarga.headers);
        if (!uploadResponse) {
            alert("No se pudo subir el archivo");
            return;
        }

        const metadata = await guardarMetadataArchivo({
            key: datosCarga.key,
            documento: archivo,
        });

        if (!metadata) {
            alert("El archivo subio a S3, pero no se pudo guardar la metadata");
            return;
        }

        window.location.reload()
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
