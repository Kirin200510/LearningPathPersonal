import { useContext } from "react";
import { useNavigate } from "react-router-dom";

import {
    Box,
    Button,
    Card,
    CardContent,
    Chip,
    Typography
} from "@mui/material";

import AutoAwesomeRoundedIcon
    from "@mui/icons-material/AutoAwesomeRounded";

import SmartToyRoundedIcon
    from "@mui/icons-material/SmartToyRounded";

import RouteRoundedIcon
    from "@mui/icons-material/RouteRounded";

import CalendarMonthRoundedIcon
    from "@mui/icons-material/CalendarMonthRounded";

import ArrowForwardRoundedIcon
    from "@mui/icons-material/ArrowForwardRounded";

import {
    MyUserContext
} from "../configs/Contexts";


const Dashboard = () => {

    const { user } =
        useContext(
            MyUserContext
        );

    const navigate =
        useNavigate();


    const features = [
        {
            title:
                "AI Learning Assistant",

            description:
                "Trao đổi với AI để xác định mục tiêu và nhận chương trình học phù hợp.",

            icon:
                <SmartToyRoundedIcon />,

            path:
                "/assistant",

            color:
                "#6366f1",

            background:
                "#eef2ff"
        },

        {
            title:
                "Learning Path",

            description:
                "Xem lộ trình học tập đã được hệ thống cá nhân hóa cho bạn.",

            icon:
                <RouteRoundedIcon />,

            path:
                "/learning-path",

            color:
                "#0ea5e9",

            background:
                "#f0f9ff"
        },

        {
            title:
                "Study Schedule",

            description:
                "Theo dõi lịch học của từng khóa học dựa trên thời gian bạn có thể học.",

            icon:
                <CalendarMonthRoundedIcon />,

            path:
                "/schedule",

            color:
                "#10b981",

            background:
                "#ecfdf5"
        }
    ];


    return (
        <Box
            sx={{
                p: {
                    xs: 2,
                    md: 4
                },

                maxWidth: 1400,
                mx: "auto"
            }}
        >

            {/* Hero */}
            <Box
                sx={{
                    position: "relative",
                    overflow: "hidden",

                    p: {
                        xs: 3,
                        md: 5
                    },

                    borderRadius: 5,

                    background:
                        "linear-gradient(135deg, #eef2ff 0%, #f0fdf4 100%)",

                    border:
                        "1px solid #e7e9f5",

                    mb: 4
                }}
            >

                {/* decoration */}
                <Box
                    sx={{
                        position:
                            "absolute",

                        width: 260,
                        height: 260,

                        borderRadius:
                            "50%",

                        background:
                            "rgba(99, 102, 241, 0.08)",

                        top: -120,
                        right: -80
                    }}
                />


                <Box
                    sx={{
                        position:
                            "relative",

                        zIndex: 1,

                        maxWidth:
                            700
                    }}
                >

                    <Chip
                        icon={
                            <AutoAwesomeRoundedIcon />
                        }

                        label="AI-powered learning"

                        sx={{
                            mb: 2,
                            bgcolor:
                                "rgba(99,102,241,0.10)",

                            color:
                                "#4f46e5",

                            fontWeight:
                                700
                        }}
                    />


                    <Typography
                        variant="h3"
                        fontWeight={800}
                        sx={{
                            mb: 2,
                            lineHeight: 1.15
                        }}
                    >
                        Xin chào{" "}

                        <Box
                            component="span"
                            sx={{
                                background:
                                    "linear-gradient(135deg, #4f46e5, #10b981)",

                                WebkitBackgroundClip:
                                    "text",

                                WebkitTextFillColor:
                                    "transparent"
                            }}
                        >
                            {user?.username}
                        </Box>

                        👋
                    </Typography>


                    <Typography
                        variant="h6"
                        color="text.secondary"
                        sx={{
                            fontWeight: 400,
                            lineHeight: 1.7,
                            mb: 3
                        }}
                    >
                        Xây dựng lộ trình học tập
                        cá nhân hóa, nhận tư vấn từ
                        AI và sắp xếp lịch học phù
                        hợp với thời gian của bạn.
                    </Typography>


                    <Button
                        variant="contained"
                        size="large"

                        endIcon={
                            <ArrowForwardRoundedIcon />
                        }

                        onClick={() =>
                            navigate(
                                "/assistant"
                            )
                        }

                        sx={{
                            px: 3,
                            py: 1.3,

                            borderRadius:
                                3,

                            textTransform:
                                "none",

                            fontWeight:
                                700,

                            boxShadow:
                                "0 8px 20px rgba(79,70,229,0.25)"
                        }}
                    >
                        Bắt đầu với AI
                    </Button>

                </Box>

            </Box>


            {/* title */}
            <Box sx={{ mb: 2.5 }}>

                <Typography
                    variant="h5"
                    fontWeight={800}
                >
                    Khám phá LearningPath
                </Typography>

                <Typography
                    color="text.secondary"
                    mt={0.5}
                >
                    Các công cụ giúp bạn xây dựng
                    và quản lý kế hoạch học tập.
                </Typography>

            </Box>


            {/* Feature Cards */}
            <Box
                sx={{
                    display: "grid",

                    gridTemplateColumns: {
                        xs:
                            "1fr",

                        md:
                            "repeat(3, 1fr)"
                    },

                    gap: 3
                }}
            >

                {features.map(
                    (feature) => (

                        <Card
                            key={
                                feature.title
                            }

                            onClick={() =>
                                navigate(
                                    feature.path
                                )
                            }

                            sx={{
                                borderRadius:
                                    4,

                                border:
                                    "1px solid #e8eaf0",

                                boxShadow:
                                    "0 4px 20px rgba(15, 23, 42, 0.04)",

                                cursor:
                                    "pointer",

                                transition:
                                    "all 0.25s ease",

                                "&:hover": {
                                    transform:
                                        "translateY(-6px)",

                                    boxShadow:
                                        "0 16px 35px rgba(15, 23, 42, 0.10)"
                                }
                            }}
                        >

                            <CardContent
                                sx={{
                                    p: 3
                                }}
                            >

                                <Box
                                    sx={{
                                        width: 52,
                                        height: 52,

                                        display:
                                            "flex",

                                        alignItems:
                                            "center",

                                        justifyContent:
                                            "center",

                                        borderRadius:
                                            3,

                                        bgcolor:
                                            feature.background,

                                        color:
                                            feature.color,

                                        mb: 2
                                    }}
                                >
                                    {
                                        feature.icon
                                    }
                                </Box>


                                <Typography
                                    variant="h6"
                                    fontWeight={700}
                                    mb={1}
                                >
                                    {
                                        feature.title
                                    }
                                </Typography>


                                <Typography
                                    variant="body2"
                                    color="text.secondary"
                                    sx={{
                                        lineHeight:
                                            1.7,

                                        minHeight:
                                            70
                                    }}
                                >
                                    {
                                        feature.description
                                    }
                                </Typography>


                                <Button
                                    endIcon={
                                        <ArrowForwardRoundedIcon />
                                    }

                                    sx={{
                                        mt: 2,
                                        px: 0,

                                        textTransform:
                                            "none",

                                        fontWeight:
                                            700,

                                        color:
                                            feature.color
                                    }}
                                >
                                    Khám phá
                                </Button>

                            </CardContent>

                        </Card>

                    )
                )}

            </Box>

        </Box>
    );
};


export default Dashboard;