import {BrowserRouter, Routes, Route, Navigate} from 'react-router-dom';
import { ArchivosPage } from './pages/ArchivosPage';


function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={ <Navigate to={'/archivos'} /> } />
                <Route path='/archivos' element={ <ArchivosPage/> } />
            </Routes>
        </BrowserRouter>
    )
}

export default App;
