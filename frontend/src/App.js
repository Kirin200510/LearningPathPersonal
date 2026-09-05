import { Navigate, Route, Routes } from "react-router-dom";
import { useContext } from "react";
import { CircularProgress, Box } from "@mui/material";

import Login from "./screens/User/Login";
import Assistant from "./screens/Assistant/Assistant";
import LearningPath from "./screens/LearningPath/LearningPath";
import Schedule from "./screens/Schedule/Schedule";
import Courses from "./screens/Courses/Courses";
import Dashboard from "./screens/DashBoard";
import MainLayout from "./layouts/MainLayout";
import Register from "./screens/User/Register";
import Profile from "./screens/User/Profile";

import { MyUserContext } from "./configs/Contexts";

function App() {
    const { user, loading } = useContext(MyUserContext);

    if (loading) {
        return (
            <Box
                sx={{
                    height: "100vh",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center"
                }}
            >
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Routes>

            {/* Nếu chưa đăng nhập thì ở Login.
                Nếu đã đăng nhập thì không cho quay lại Login */}
            <Route
                path="/login"
                element={user ? <Navigate to="/" replace /> : <Login />}
            />
            <Route
                path="/register"
                element={user ? <Navigate to="/" replace /> : <Register />}
            />

            {/* Tất cả trang bên trong đều bắt buộc đăng nhập */}
            <Route
                element={
                    user
                        ? <MainLayout />
                        : <Navigate to="/login" replace />
                }
            >
                <Route path="/" element={<Dashboard />} />
                <Route path="/assistant" element={<Assistant />} />
                <Route path="/learning-path" element={<LearningPath />} />
                <Route path="/schedule" element={<Schedule />} />
                <Route path="/courses" element={<Courses />} />
                <Route path="/profile" element={<Profile />}/>
            </Route>

            {/* URL không tồn tại */}
            <Route
                path="*"
                element={<Navigate to={user ? "/" : "/login"} replace />}
            />
        </Routes>
    );
}

export default App;