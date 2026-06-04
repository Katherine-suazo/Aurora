import { ArchivosList } from "../components/ArchivosLista";
import { ArchivoFormPage } from "../components/ArchivoFormPage";

export function ArchivosPage() {
    return (
        <div>
            <ArchivoFormPage />
            <ArchivosList />
        </div>
    )
}