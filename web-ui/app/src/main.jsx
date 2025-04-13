import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import App from './App.jsx'
import {APIProvider} from "@vis.gl/react-google-maps";

const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_API_TOKEN;

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <APIProvider apiKey={GOOGLE_MAPS_API_KEY}>
            <App/>
        </APIProvider>
    </StrictMode>,
)
