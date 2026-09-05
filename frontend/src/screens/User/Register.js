import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {Alert, Box, Button, Paper, TextField, Typography} from "@mui/material";
import Apis, { endpoints } from "../../configs/Apis";

const Register = () => {
    const navigate = useNavigate();
     const [user, setUser] = useState({
        username: "",
        email: "",
        password: "",
        confirmPassword: ""
    });
    const [err, setErr] = useState(null);
    const [success, setSuccess] = useState(null);
    const [loading, setLoading] = useState(false);

    const validate = () => {
        if(!user.email || !user.username || !user.password || !user.confirmPassword) {
            setErr("Vui lòng nhập đầy đủ thông tin");
            return false;
        }
        if (user.password !== user.confirmPassword) {
            setErr("Mật khẩu xác nhận không khớp.");
            return false;
        }
        setErr(null);
        return true;
    };

    const register = async () => {
        if (!validate()) return;

        try {
            setLoading(true);
            setErr(null);
            setSuccess(null);
            await Apis.post(endpoints["register"], {
                username: user.username.trim(),
                email: user.email.trim(),
                password: user.password
            });
            setSuccess("Đăng ký tài khoản thành công.");
            setTimeout(() => {
                navigate("/login");
            }, 1000);

        } catch(ex) {
            console.error(ex)
        } finally {
            setLoading(false);
        }

    };
    return (
        <Box sx={{
            minHeight: "100vh",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            bgcolor: "#f5f5f5"
        }}>
            <Paper
                elevation={3}
                sx={{
                    width: 400,
                    padding: 4,
                    borderRadius: 3
                }}
            >
                <Typography
                    variant="h4"
                    textAlign="center"
                    fontWeight="bold"
                    mb={1}
                >
                    LearningPath
                </Typography>

                <Typography
                    textAlign="center"
                    color="text.secondary"
                    mb={2}
                >
                    Tạo tài khoản mới
                </Typography>

                {err && (
                    <Alert severity="error" sx={{ mb: 2 }}>
                        {err}
                    </Alert>
                )}

                {success && (
                    <Alert severity="success" sx={{ mb: 2 }}>
                        {success}
                    </Alert>
                )}

                <TextField
                    label="Tên đăng nhập"
                    fullWidth
                    margin="normal"
                    value={user.username}
                    onChange={e =>
                        setUser({ ...user, username: e.target.value })
                    }
                />

                <TextField
                    label="Email"
                    type="email"
                    fullWidth
                    margin="normal"
                    value={user.email}
                    onChange={e =>
                        setUser({ ...user, email: e.target.value })
                    }
                />

                <TextField
                    label="Mật khẩu"
                    type="password"
                    fullWidth
                    margin="normal"
                    value={user.password}
                    onChange={e =>
                        setUser({ ...user, password: e.target.value })
                    }
                />

                <TextField
                    label="Xác nhận mật khẩu"
                    type="password"
                    fullWidth
                    margin="normal"
                    value={user.confirmPassword}
                    onChange={e =>
                        setUser({ ...user, confirmPassword: e.target.value })
                    }
                />

                <Button
                    variant="contained"
                    fullWidth
                    size="large"
                    disabled={loading}
                    onClick={register}
                    sx={{ mt: 2 }}
                >
                    {loading ? "Đang đăng ký..." : "Đăng ký"}
                </Button>

                <Box sx={{ textAlign: "center", mt: 2 }}>
                    <Typography
                        component="span"
                        variant="body2"
                        color="text.secondary"
                    >
                        Đã có tài khoản?{" "}
                    </Typography>

                    <Button
                        variant="text"
                        onClick={() => navigate("/login")}
                        sx={{
                            textTransform: "none",
                            p: 0,
                            minWidth: 0,
                            fontWeight: 700
                        }}
                    >
                        Đăng nhập
                    </Button>
                </Box>
            </Paper>
        </Box>
    );
};
export default Register;