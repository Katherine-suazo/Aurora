import { getAllArchivos } from "../api/apiFile";
import { useEffect, useState } from "react";


export function ArchivosList() {
    const [archivos, setArchivos] = useState([]);
    const [campoOrden, setCampoOrden] = useState("nombre");
    const [direccionOrden, setDireccionOrden] = useState("asc");

    useEffect(() => { cargarArchivos() }, []);

    const cargarArchivos = async () => {
        const data = await getAllArchivos();
        setArchivos(data || []);
    };

    if (archivos.length === 0) {
        return <p>No hay archivos registrados</p>
    };

    const archivosOrdenados = [...archivos].sort((a, b) => {
        let resultado = 0;
        if (campoOrden === "nombre") {
            resultado = a.nombre.localeCompare(b.nombre);
        }
        if (campoOrden === "tamaño") {
            resultado = a.tamaño - b.tamaño;
        }
        if (campoOrden === "fecha_subida") {
            resultado = new Date(a.fecha_subida) - new Date(b.fecha_subida);
        }
        return direccionOrden === "asc" ? resultado : -resultado;
    });

    return (
        <div className="container" >
            <h2>Lista de Archivos</h2>

            <div className="filtros">

                <label>Ordenar por:</label>
                <select value={campoOrden} onChange={(e) => setCampoOrden(e.target.value)}>
                    <option value="nombre">Nombre</option>
                    <option value="tamaño">Tamaño</option>
                    <option value="fecha_subida">Fecha</option>
                </select>

                <label>Dirección:</label>
                <select value={direccionOrden} onChange={(e) => setDireccionOrden(e.target.value)} >
                    <option value="asc">Ascendente</option>
                    <option value="desc">Descendente</option>
                </select>

            </div>

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
                        {archivosOrdenados.map((archivo) => (

                            <tr key={archivo.id} >
                                <td> {archivo.nombre} </td>
                                <td> {(archivo.tamaño / 1024 / 1024).toFixed(2)} MB </td>
                                <td> {new Date(archivo.fecha_subida).toLocaleDateString()} </td>
                            </tr>

                        ))}
                    </tbody>

                </table>
            )}

        </div>
    )
}


