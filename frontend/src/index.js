import React from "react";
import ReactDOM from "react-dom/client";
import {BrowserRouter} from "react-router-dom";
import {CssBaseline} from "@mui/material";
import App from "./App";

import {UserProvider} from "./configs/Contexts";


const root = ReactDOM.createRoot(
    document.getElementById("root")
);


root.render(
    <React.StrictMode>

        <UserProvider>

            <BrowserRouter>

                <CssBaseline />

                <App />

            </BrowserRouter>

        </UserProvider>

    </React.StrictMode>
);