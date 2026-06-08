import { ArchivosList } from "../components/ArchivosLista";
import { ArchivoFormPage } from "../components/ArchivoFormPage";

export function ArchivosPage() {
    return (
        <div>
            <ArchivoFormPage />  # para subir el archivo
            <ArchivosList />     # mustra listado de los archivos
        </div>
    )
}