import { useEffect, useState } from "react";
import { getAllArchivos } from "../api/apiFile";

export function ArchivosList() {
    const [archivos, setArchivos] = useState([]);

    useEffect(() => {
        async function cargarArchivos() {
            try {
                const respuesta = await getAllArchivos();
                console.log(respuesta.data);
                setArchivos(respuesta.data);
            }
            catch (error) {
                console.log('Error en cargar archivos', error)
            }
        }
        cargarArchivos();

    }, []);

    return (
        <div>
            {archivos.map((archivo) => (
                <div key={archivo.id}> {archivo.nombre} </div>
            ))}
        </div>
    )

}