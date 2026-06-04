import {BrowserRouter, Routes, Route} from 'react-router-dom';
import {ArchivoFormPage} from "./pages/ArchivoFormPage";


function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/' element={<ArchivoFormPage/>} />
            </Routes>
        </BrowserRouter>
    )
}

export default App;
