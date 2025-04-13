import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import App from './App.jsx'
import {APIProvider} from "@vis.gl/react-google-maps";
import {GOOGLE_API_TOKEN} from './config/index.js';

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <APIProvider apiKey={GOOGLE_API_TOKEN}>
            <App/>
        </APIProvider>
    </StrictMode>,
)
