import {useContext} from "react";
import {useNavigate} from "react-router-dom";
import {Box,Button,Typography} from "@mui/material";
import {MyUserContext} from "../configs/Contexts";

const Home = () => {
    const {user,dispatch} =useContext(MyUserContext);

    const navigate =useNavigate();


    const logout = () => {
        localStorage.removeItem("token");
        dispatch({
            type: "logout"
        });
        navigate("/login");
    };

    return (
        <Box sx={{ p: 5 }}>

            <Typography variant="h4">
                Xin chào {user?.username}
            </Typography>


            <Button
                variant="outlined"
                color="error"
                sx={{ mt: 3 }}
                onClick={logout}
            >
                Đăng xuất
            </Button>
        </Box>
    );
};


export default Home;