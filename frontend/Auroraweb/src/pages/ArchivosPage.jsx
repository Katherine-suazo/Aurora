import { ArchivosList } from "../components/ArchivosLista";
import { ArchivoForm } from "../components/ArchivoForm";
import "../style/Estilo.css"

export function ArchivosPage() {
    return (
        <div className="body">

            <h1 className="titulo">Cloud</h1>
            <ArchivoForm /> 
            <ArchivosList /> 

        </div>
    )
}