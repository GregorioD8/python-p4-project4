import React from "react";
import { createRoot } from "react-dom/client";
import App from "./components/App";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./components/AuthContext";
import "./index.css";
import 'bootstrap/dist/css/bootstrap.min.css';

const container = document.getElementById("root");
const root = createRoot(container);
root.render(
    <AuthProvider>
        <BrowserRouter>
            <App />
        </BrowserRouter>
    </AuthProvider>
);
