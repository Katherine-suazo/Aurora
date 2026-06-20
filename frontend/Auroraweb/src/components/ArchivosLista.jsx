import { obtenerListaArchivos } from "../api/apiFile";
import { useEffect, useState } from "react";
import "../style/Estilo.css"


export function ArchivosList() {
    const [archivos, setArchivos] = useState([]);
    const [campoOrden, setCampoOrden] = useState("nombre");
    const [direccionOrden, setDireccionOrden] = useState("asc");

    useEffect(() => { cargarArchivos() }, []);

    const cargarArchivos = async () => {
        const data = await obtenerListaArchivos();
        setArchivos(data.archivos || []);
    };

    if (archivos.length === 0) {
        return <p className="container" >No hay archivos registrados</p>
    };

    const archivosOrdenados = [...archivos].sort((a, b) => {
        let resultado = 0;
        if (campoOrden === "nombre") {
            resultado = a.nombre.localeCompare(b.nombre);
        }
        if (campoOrden === "tamano_bytes") {
            resultado = a.tamano_bytes - b.tamano_bytes;
        }
        if (campoOrden === "ultima_modificacion") {
            resultado = new Date(a.ultima_modificacion) - new Date(b.ultima_modificacion);
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

                            <tr key={archivo.nombre} >
                                <td> {archivo.nombre} </td>
                                <td> {(archivo.tamano_bytes / 1024 / 1024).toFixed(2)} MB </td>
                                <td> {new Date(archivo.ultima_modificacion).toLocaleDateString()} </td>
                            </tr>

                        ))}
                    </tbody>

                </table>
            )}

        </div>
    )
}


