import {useContext,useState} from "react";
import {useNavigate} from "react-router-dom";
import {Alert,Box,Button,Paper,TextField,Typography} from "@mui/material";
import Apis, {authApis,endpoints} from "../../configs/Apis";
import { MyUserContext} from "../../configs/Contexts";

const Login = () => {
    const { dispatch} = useContext(MyUserContext);
    const [user, setUser] = useState({
        username: "",
        password: ""
    });
    const [err, setErr] =useState(null);
    const [loading, setLoading] =useState(false);
    const navigate =useNavigate();
    
     const validate = () => {
        if (!user.username) {
            setErr('Vui lòng nhập tên đăng nhập');
            return false;
        } else if (!user.password) {
            setErr('Vui lòng nhập mật khẩu!');
            return false;
        } else {
            setErr(null);
            return true;
        }
    }

    const login = async () => {
        if (validate()) {
            try {
                setLoading(true);
                setErr(null);
                const formData = new URLSearchParams();
                formData.append("username", user.username);
                formData.append("password", user.password);
                const res = await Apis.post(endpoints["login"],formData,
                {
                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded"
                    }
                });
                const token = res.data.access_token;
                //Save token
                localStorage.setItem("token", token);
                
                let u = await authApis(token).get(endpoints["current-user"]);
                 //Lưu user vào Context
                dispatch({
                    type: "login",
                    payload: u.data
                });
                navigate("/");
            } catch (ex) {
                console.error(ex);
                setErr("Tên đăng nhập hoặc mật khẩu không chính xác.");
            } finally {
                setLoading(false);
            }
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
            <Paper elevation={3}
                sx={{
                    width: 400,
                    padding: 4,
                    borderRadius: 3
                }}>
                <Typography variant="h4"
                    textAlign="center"
                    fontWeight="bold"
                    mb={3}>
                    LearningPath
                </Typography>

                {err && ( <Alert severity="error" sx={{ mb: 2 }}>
                        {err}
                        </Alert>
                )}
                <TextField
                    label="Tên đăng nhập"
                    fullWidth
                    margin="normal"
                    value={user.username}
                    onChange={(e) =>
                        setUser({...user, username:e.target.value})
                    }
                />
                <TextField
                    label="Mật khẩu"
                    type="password"
                    fullWidth
                    margin="normal"
                    value={user.password}
                    onChange={(e) =>
                        setUser({...user,password:e.target.value})
                    }
                />
                <Button
                    variant="contained"
                    fullWidth
                    size="large"
                    sx={{ mt: 2 }}
                    disabled={loading}
                    onClick={login}
                >
                    {loading ? "Đang đăng nhập...": "Đăng nhập"}
                </Button>
                <Box sx={{ textAlign: "center", mt: 2 }}>
                    <Typography
                        component="span"
                        variant="body2"
                        color="text.secondary"
                    >
                        Chưa có tài khoản?{" "}
                    </Typography>

                    <Button
                        variant="text"
                        onClick={() => navigate("/register")}
                        sx={{
                            textTransform: "none",
                            p: 0,
                            minWidth: 0,
                            fontWeight: 700
                        }}
                    >
                        Đăng ký
                    </Button>
                </Box>
            </Paper>
        </Box>
    );

}
export default Login;