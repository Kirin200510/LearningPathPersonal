import {useContext,useEffect,useState} from "react";
import {useNavigate} from "react-router-dom";
import {Alert,Avatar,Box,Button,CircularProgress,Divider,Paper,TextField,Typography} from "@mui/material";
import PersonRoundedIcon from "@mui/icons-material/PersonRounded";
import LockRoundedIcon from "@mui/icons-material/LockRounded";
import {authApis,endpoints} from "../../configs/Apis";
import {MyUserContext} from "../../configs/Contexts";

const Profile = () => {
    const {user,dispatch} = useContext(MyUserContext);
    const navigate = useNavigate();

    const [profile,setProfile] = useState({username:"",email:""});
    const [passwordForm,setPasswordForm] = useState({old_password:"",new_password:"",confirm_password:""});
    const [loading,setLoading] = useState(true);
    const [saving,setSaving] = useState(false);
    const [changingPassword,setChangingPassword] = useState(false);
    const [profileError,setProfileError] = useState("");
    const [profileSuccess,setProfileSuccess] = useState("");
    const [passwordError,setPasswordError] = useState("");
    const [passwordSuccess,setPasswordSuccess] = useState("");

    const loadProfile = async () => {
        try {
            setLoading(true);
            const token = localStorage.getItem("token");
            const res = await authApis(token).get(endpoints["profile"]);
            setProfile({username:res.data.username || "",email:res.data.email || ""});
        } catch (error) {
            console.error(error);
            setProfileError("Không thể tải thông tin cá nhân.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(()=> {
        loadProfile();
    },[]);

    const updateProfile = async() =>{
        const username = profile.username.trim();
        const email = profile.email.trim();

        if (!username || !email) {
            setProfileError("Vui lòng nhập đầy đủ thông tin.");
            return;
        }
        try {
            setSaving(true);
            const token = localStorage.getItem("token");
            const usernameChanged = username !== user?.username;

            const res = await authApis(token).patch(endpoints["profile"],{username,email});
            if (usernameChanged) {
                setProfileSuccess("Đổi tên đăng nhập thành công. Vui lòng đăng nhập lại.");

                setTimeout(() => {
                    localStorage.removeItem("token");
                    dispatch({type:"logout"});
                    navigate("/login");
                },1500);
                return;
            }
            dispatch({type:"login",payload:res.data});
            setProfileSuccess("Cập nhật thông tin thành công.");
        } catch(ex) {
             console.error(ex);
        } finally {
            setSaving(false);
        }
    };

    const changePassword= async() => {
        const {old_password,new_password,confirm_password} = passwordForm;
        if (!old_password || !new_password || !confirm_password) {
            setPasswordError("Vui lòng nhập đầy đủ thông tin.");
            return;
        }
        if (new_password !== confirm_password) {
            setPasswordError("Xác nhận mật khẩu mới không khớp.");
            return;
        }

        if (old_password === new_password) {
            setPasswordError("Mật khẩu mới phải khác mật khẩu hiện tại.");
            return;
        }
        try {
            setChangingPassword(true);
            const token = localStorage.getItem("token");

            await authApis(token).post(endpoints["change-password"],{
                old_password,
                new_password
            });

            setPasswordForm({old_password:"",new_password:"",confirm_password:""});
            setPasswordSuccess("Đổi mật khẩu thành công.");
        } catch (ex) {
            console.error(ex);
        } finally {
            setChangingPassword(false);
        }
    };
    if (loading) {
        return (
            <Box sx={{display:"flex",justifyContent:"center",mt:8}}>
                <CircularProgress />
            </Box>
        );
    }
     return (
        <Box sx={{p:4,maxWidth:900,mx:"auto"}}>
            <Box sx={{mb:4}}>
                <Typography variant="h4" fontWeight={800}>Hồ sơ cá nhân</Typography>
                <Typography color="text.secondary" sx={{mt:1}}>Xem và cập nhật thông tin tài khoản.</Typography>
            </Box>

            <Paper elevation={0} sx={{p:4,border:"1px solid #e8eaf0",borderRadius:4,mb:3}}>
                <Box sx={{display:"flex",alignItems:"center",gap:2,mb:3}}>
                    <Avatar sx={{width:64,height:64,bgcolor:"primary.main",fontSize:26,fontWeight:800}}>
                        {profile.username?.charAt(0)?.toUpperCase()}
                    </Avatar>

                    <Box>
                        <Typography variant="h6" fontWeight={800}>{profile.username}</Typography>
                        <Typography color="text.secondary">{profile.email}</Typography>
                    </Box>
                </Box>

                <Divider sx={{mb:3}} />

                <Box sx={{display:"flex",alignItems:"center",gap:1,mb:2}}>
                    <PersonRoundedIcon color="primary" />
                    <Typography variant="h6" fontWeight={800}>Thông tin cá nhân</Typography>
                </Box>

                {profileError && <Alert severity="error" sx={{mb:2}}>{profileError}</Alert>}
                {profileSuccess && <Alert severity="success" sx={{mb:2}}>{profileSuccess}</Alert>}

                <TextField label="Tên đăng nhập" fullWidth margin="normal" value={profile.username}
                    onChange={e => setProfile({...profile,username:e.target.value})} />

                <TextField label="Email" type="email" fullWidth margin="normal" value={profile.email}
                    onChange={e => setProfile({...profile,email:e.target.value})} />

                <Button variant="contained" disabled={saving} onClick={updateProfile}
                    sx={{mt:2,px:3,borderRadius:2.5,textTransform:"none",fontWeight:700}}>
                    {saving ? "Đang lưu..." : "Lưu thay đổi"}
                </Button>
            </Paper>

            <Paper elevation={0} sx={{p:4,border:"1px solid #e8eaf0",borderRadius:4}}>
                <Box sx={{display:"flex",alignItems:"center",gap:1,mb:2}}>
                    <LockRoundedIcon color="primary" />
                    <Typography variant="h6" fontWeight={800}>Đổi mật khẩu</Typography>
                </Box>

                {passwordError && <Alert severity="error" sx={{mb:2}}>{passwordError}</Alert>}
                {passwordSuccess && <Alert severity="success" sx={{mb:2}}>{passwordSuccess}</Alert>}

                <TextField label="Mật khẩu hiện tại" type="password" fullWidth margin="normal"
                    value={passwordForm.old_password}
                    onChange={e => setPasswordForm({...passwordForm,old_password:e.target.value})} />

                <TextField label="Mật khẩu mới" type="password" fullWidth margin="normal"
                    value={passwordForm.new_password}
                    onChange={e => setPasswordForm({...passwordForm,new_password:e.target.value})} />

                <TextField label="Xác nhận mật khẩu mới" type="password" fullWidth margin="normal"
                    value={passwordForm.confirm_password}
                    onChange={e => setPasswordForm({...passwordForm,confirm_password:e.target.value})} />

                <Button variant="contained" disabled={changingPassword} onClick={changePassword}
                    sx={{mt:2,px:3,borderRadius:2.5,textTransform:"none",fontWeight:700}}>
                    {changingPassword ? "Đang đổi..." : "Đổi mật khẩu"}
                </Button>
            </Paper>
        </Box>
    );
};
export default Profile;