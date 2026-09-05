import { useContext } from "react";
import {NavLink,useLocation,useNavigate} from "react-router-dom";
import { Avatar,Box,Button,Divider,Drawer,List,ListItem,ListItemButton,ListItemIcon,ListItemText,Typography} from "@mui/material";
import DashboardRoundedIcon from "@mui/icons-material/DashboardRounded";
import SmartToyRoundedIcon from "@mui/icons-material/SmartToyRounded";
import RouteRoundedIcon from "@mui/icons-material/RouteRounded";
import CalendarMonthRoundedIcon from "@mui/icons-material/CalendarMonthRounded";
import SchoolRoundedIcon from "@mui/icons-material/SchoolRounded";
import LogoutRoundedIcon from "@mui/icons-material/LogoutRounded";
import {MyUserContext} from "../configs/Contexts";

export const drawerWidth = 260;

const Sidebar = () => {

    const {user,dispatch} = useContext(MyUserContext);
    const location =
        useLocation();
    const navigate =
        useNavigate();
    const menuItems = [
        {
            text: "Dashboard",
            icon: <DashboardRoundedIcon />,
            path: "/"
        },
        {
            text: "AI Assistant",
            icon: <SmartToyRoundedIcon />,
            path: "/assistant"
        },
        {
            text: "Learning Path",
            icon: <RouteRoundedIcon />,
            path: "/learning-path"
        },
        {
            text: "Schedule",
            icon: <CalendarMonthRoundedIcon />,
            path: "/schedule"
        },{
            text: "Courses",
            icon: <SchoolRoundedIcon />,
            path: "/courses"
        },
    ];

    const logout = () => {
        localStorage.removeItem("token");
        dispatch({
            type: "logout"
        });
        navigate("/login");
    };

    return (
        <Drawer
            variant="permanent"
            sx={{
                width: drawerWidth,
                flexShrink: 0,
                "& .MuiDrawer-paper": {
                    width: drawerWidth,
                    boxSizing: "border-box",
                    borderRight:"1px solid #e8eaf0",
                    background:"linear-gradient(180deg, #ffffff 0%, #f8f9ff 100%)"
                }
            }}
        >
            {/* Logo */}
            <Box
                sx={{
                    px: 3,
                    py: 3,
                    display: "flex",
                    alignItems: "center",
                    gap: 1.5
                }}
            >

                <Box
                    sx={{
                        width: 42,
                        height: 42,
                        borderRadius: 2.5,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        color: "white",
                        background:"linear-gradient(135deg, #6366f1, #10b981)",
                        boxShadow:"0 8px 20px rgba(99, 102, 241, 0.25)"
                    }}
                >
                    <SchoolRoundedIcon />
                </Box>
                <Box>
                    <Typography
                        variant="h6"
                        fontWeight={800}
                        sx={{
                            lineHeight: 1.1,
                            background:"linear-gradient(135deg, #4f46e5, #10b981)",
                            WebkitBackgroundClip:"text",
                            WebkitTextFillColor:"transparent"
                        }}
                    >
                        LearningPath
                    </Typography>

                    <Typography
                        variant="caption"
                        color="text.secondary">
                        AI Learning Assistant
                    </Typography>
                </Box>
            </Box>
            <Divider />
            {/* Menu */}
            <List
                sx={{
                    px: 2,
                    py: 2,
                    flexGrow: 1
                }}
            >
                <Typography
                    variant="caption"
                    sx={{
                        px: 1.5,
                        mb: 1,
                        display: "block",
                        color: "#94a3b8",
                        fontWeight: 700,
                        letterSpacing: 1
                    }}
                >
                    MENU
                </Typography>
                {menuItems.map((item) => {
                    const active =location.pathname === item.path;

                    return (
                        <ListItem
                            key={item.path}
                            disablePadding
                            sx={{ mb: 0.7 }}
                        >
                            <ListItemButton
                                component={NavLink}
                                to={item.path}
                                sx={{
                                    borderRadius: 2.5,
                                    minHeight: 48,
                                    color: active? "#4f46e5": "#64748b",
                                    backgroundColor:active? "rgba(79, 70, 229, 0.10)": "transparent",
                                    transition:"all 0.2s ease",
                                    "&:hover": {
                                        backgroundColor:active? "rgba(79, 70, 229, 0.13)": "rgba(79, 70, 229, 0.05)",
                                        color:"#4f46e5",
                                        transform:"translateX(3px)"
                                    }
                                }}
                            >
                                <ListItemIcon
                                    sx={{
                                        minWidth: 40,
                                        color: "inherit"
                                    }}
                                >
                                    {item.icon}
                                </ListItemIcon>
                                <ListItemText
                                    primary={item.text}
                                    primaryTypographyProps={{fontWeight:active? 700: 500
                                    }}
                                />
                            </ListItemButton>
                        </ListItem>
                    );
                })}

            </List>
            {/* User */}
            <Box
                onClick={() => navigate("/profile")}
                sx={{
                    p: 1.5,
                    display: "flex",
                    alignItems: "center",
                    gap: 1.5,
                    borderRadius: 3,
                    bgcolor: "white",
                    border: "1px solid #e8eaf0",
                    cursor: "pointer",
                    transition: "all 0.2s ease",

                    "&:hover": {
                        bgcolor: "rgba(79, 70, 229, 0.05)",
                        borderColor: "rgba(79, 70, 229, 0.25)"
                    }
                }}
            >
                    <Avatar
                        sx={{
                            width: 40,
                            height: 40,
                            bgcolor:"primary.main",
                            fontWeight: 700
                        }}
                    >
                        {user?.username?.charAt(0)?.toUpperCase()}
                    </Avatar>
                    <Box
                        sx={{
                            flexGrow: 1,
                            minWidth: 0
                        }}
                    >
                        <Typography
                            variant="body2"
                            fontWeight={700}
                            noWrap
                        >
                            {user?.username}
                        </Typography>
                        <Typography
                            variant="caption"
                            color="text.secondary"
                        >
                            Student
                        </Typography>
                    </Box>


                    <Button
                        onClick={e => {
                            e.stopPropagation();
                            logout();
                        }}
                        sx={{
                            minWidth: 36,
                            width: 36,
                            height: 36,
                            borderRadius: 2
                        }}
                    >
                        <LogoutRoundedIcon fontSize="small" />
                    </Button>
            </Box>

        </Drawer>
    );
};


export default Sidebar;