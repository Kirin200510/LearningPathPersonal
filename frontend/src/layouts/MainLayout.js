import {
    Box
} from "@mui/material";

import {
    Outlet
} from "react-router-dom";

import Sidebar, {
    drawerWidth
} from "../components/Sidebar";


const MainLayout = () => {

    return (
        <Box
            sx={{
                minHeight: "100vh",
                bgcolor: "#f8fafc"
            }}
        >

            <Sidebar />


            <Box
                component="main"
                sx={{
                    ml:
                        `${drawerWidth}px`,

                    minHeight:
                        "100vh"
                }}
            >

                <Outlet />

            </Box>

        </Box>
    );
};


export default MainLayout;