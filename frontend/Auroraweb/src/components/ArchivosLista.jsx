import { getAllArchivos } from "../api/apiFile";

export function ArchivosList({ archivo }) {

    return (
        <div>
            {archivo && (
                <table>
                    <thead>
                        <tr>
                            <th> Nombre </th>
                            <th> Tamaño </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td> {archivo.name} </td>
                            <td> {(archivo.size / 1024 / 1024).toFixed(2)} MB </td>
                        </tr>
                    </tbody>

                </table>
            )}

        </div>
    )

}


