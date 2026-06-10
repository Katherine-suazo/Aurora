import { getAllArchivos } from "../api/apiFile";
import { useEffect, useState } from "react";

export function ArchivosList() {

    const [archivos, setArchivos] = useState([]);

    useEffect(() => { cargarArchivos() }, []);

    const cargarArchivos = async () => {
        const data = await getAllArchivos();
        setArchivos(data || []);
    };

    if (archivos.length === 0) {
        return <p>No hay archivos registrados</p>
    };

    return (
        <div className="container" >
            <h2>Lista de Archivos</h2>
            {archivos && (
                <table>

                    <thead>
                        <tr>
                            <th> Nombre </th>
                            <th> Tamaño </th>
                            <th> Fecha </th>
                        </tr>
                    </thead>

                    <tbody>
                        {archivos.map((archivo) => (

                            <tr key={ archivo.id } >
                                <td> { archivo.nombre } </td>
                                <td> { (archivo.tamaño / 1024 / 1024).toFixed(2) } MB </td>
                                <td> { new Date(archivo.fecha_subida).toLocaleDateString() } </td>
                            </tr>

                        ))}
                    </tbody>

                </table>
            )}

        </div>
    )
}


