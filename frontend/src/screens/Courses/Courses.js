import React, {useEffect,useState} from "react";
import {Box,Typography,Card,CardContent,CircularProgress,TextField,InputAdornment,Chip,Button} from "@mui/material";
import SearchRoundedIcon from "@mui/icons-material/SearchRounded";
import AccessTimeRoundedIcon from "@mui/icons-material/AccessTimeRounded";
import SchoolRoundedIcon from "@mui/icons-material/SchoolRounded";
import {authApis,endpoints} from "../../configs/Apis";

const CoursesScreen= () =>{
    const [courses,setCourses] = useState([]);
    const [loading,setLoading] = useState(false);
    const [q, setQ] = useState("");
    const [page, setPage] = useState(1);

    const loadCourses= async() => {
        try {
            setLoading(true);
            const token=localStorage.getItem("token");
            let url= `${endpoints["courses"]}?page=${page}&size=9`;
            if (q.trim()) {
                url +=`&search=${q.trim()}`;
            }
            console.info("Course API:",url);
            const res =await authApis(token).get(url);
            if (res.data.page>=res.data.pages) {
                setPage(0);
            }
            if (page===1) {
                setCourses(res.data.items || []);
            } else if (page>1) {
                setCourses(prev => [...prev,...(res.data.items || [])])
            }
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        let timer = setTimeout(() => {
            if (page > 0)
                loadCourses();
        }, 500);

        return () => clearTimeout(timer);
    }, [q, page]);

    useEffect(() => {
        setPage(1);
    }, [q]);

    const loadMore = () => {
        if (page > 0 && !loading)
            setPage(page + 1);
    };
    return (
        <Box
            sx={{
                p: {xs: 2, md: 4},
                minHeight: "100vh",
                bgcolor:"#f8fafc"
            }}
        >
            {/* ================= HEADER ================= */}
            <Box sx={{ mb: 4 }}>
                <Box
                    sx={{
                        display:"flex",
                        alignItems: "center",
                        gap:1.5
                    }}>
                    <Box
                        sx={{
                            width:46,
                            height: 46,
                            borderRadius: 2.5,
                            display:"flex",
                            alignItems:"center",
                            justifyContent:"center",
                            color: "white",
                            background:"linear-gradient(135deg, #4f46e5, #10b981)",
                            boxShadow: "0 8px 20px rgba(79,70,229,0.20)"
                        }}
                    >
                        <SchoolRoundedIcon />
                    </Box>
                    <Box>
                        <Typography
                            variant="h4"
                            fontWeight={800}
                            sx={{
                                background:"linear-gradient(135deg, #4f46e5, #10b981)",
                                WebkitBackgroundClip:"text",
                                WebkitTextFillColor:"transparent"
                            }}
                        >
                            Danh sách khóa học
                        </Typography>
                        <Typography variant="body1" color="text.secondary">
                            Khám phá các khóa học phù hợp với mục tiêu học tập của bạn.
                        </Typography>
                    </Box>
                </Box>
            </Box>
            {/* ================= SEARCH ================= */}
            <Box
                sx={{
                    maxWidth:650,
                    mb: 4
                }}
            >
                <TextField
                    fullWidth
                    value={q}
                    onChange={
                        e =>setQ(e.target.value)
                    }
                    placeholder="Tìm kiếm khóa học..."
                    slotProps={{
                        input: {
                            startAdornment: (
                                <InputAdornment position="start">
                                    <SearchRoundedIcon
                                        sx={{color:"#64748b"}}
                                    />

                                </InputAdornment>
                            )
                        }
                    }}
                    sx={{
                        bgcolor:"white",
                        "& .MuiOutlinedInput-root":
                            {borderRadius: 3}
                    }}
                />
            </Box>
            {/* ================= COURSE GRID ================= */}
            <Box
                sx={{
                    display: "grid",
                    gridTemplateColumns: {
                        xs: "1fr",
                        sm: "repeat(2, minmax(0, 1fr))",
                        md: "repeat(3, minmax(0, 1fr))"
                    },
                    gap: 3,
                    // Các hàng có chiều cao đồng đều
                    gridAutoRows: "1fr"
                }}
            >
                {courses.map(course => (
                    <Card
                        key={course.id}
                        component={course.url? "a": "div"}
                        {...(
                            course.url
                                ? {
                                    href: course.url,
                                    target: "_blank",
                                    rel: "noopener noreferrer"
                                }
                                : {}
                        )}
                        sx={{
                            width: "100%",
                            height: "100%",
                            display: "flex",
                            flexDirection: "column",
                            borderRadius: 4,
                            border:"1px solid #e5e7eb",
                            boxShadow:"0 8px 25px rgba(15,23,42,0.06)",
                            overflow: "hidden",
                            textDecoration: "none",
                            color: "inherit",
                            cursor: course.url? "pointer": "default",
                            transition:"transform 0.25s ease, box-shadow 0.25s ease",
                            "&:hover": course.url
                                ? {
                                    transform:"translateY(-5px)",
                                    boxShadow:"0 14px 35px rgba(15,23,42,0.12)"
                                }
                                : {}
                        }}
                    >
                        {/* THANH MÀU TRÊN CARD */}
                        <Box
                            sx={{
                                height: 8,
                                flexShrink: 0,
                                background:"linear-gradient(90deg, #4f46e5, #10b981)"
                            }}
                        />


                        <CardContent
                            sx={{
                                p: 3,
                                flexGrow: 1,
                                display: "flex",
                                flexDirection: "column"
                            }}
                        >
                            {/* TÊN KHÓA HỌC */}
                            <Typography
                                variant="h6"
                                fontWeight={700}
                                sx={{
                                    color: "#0f172a",
                                    lineHeight: 1.45,
                                    mb: 2
                                }}
                            >
                                {course.title}
                            </Typography>
                            {/* MÔ TẢ - CHỈ HIỆN NẾU CÓ */}
                            {course.description && (
                                <Typography
                                    variant="body2"
                                    color="text.secondary"
                                    sx={{
                                        lineHeight: 1.7,
                                        mb: 2
                                    }}
                                >
                                    {course.description}
                                </Typography>
                            )}
                            {/* THÔNG TIN COURSE */}
                            <Box
                                sx={{
                                    mt: "auto",
                                    display: "flex",
                                    flexDirection: "column",
                                    gap: 1
                                }}
                            >
                                {/* THỜI LƯỢNG */}
                                {Number(course.estimated_hours) > 0 && (
                                    <Box
                                        sx={{
                                            display: "flex",
                                            alignItems: "center",
                                            gap: 0.8
                                        }}
                                    >
                                        <AccessTimeRoundedIcon
                                            sx={{
                                                fontSize: 18,
                                                color: "#64748b"
                                            }}
                                        />
                                        <Typography
                                            variant="body2"
                                            color="text.secondary"
                                            fontWeight={600}
                                        >
                                            {course.estimated_hours} giờ
                                        </Typography>
                                    </Box>
                                )}
                                {/* SOURCE ID */}
                                {course.source_id && (
                                    <Typography
                                        variant="caption"
                                        color="text.secondary"
                                        sx={{
                                            wordBreak:"break-word"
                                        }}
                                    >
                                        Nguồn: {course.source_id}
                                    </Typography>
                                )}
                                {/* CÓ LINK */}
                                {course.url && (
                                    <Chip
                                        label="Mở khóa học ↗"
                                        size="small"
                                        sx={{
                                            alignSelf:"flex-start",
                                            mt: 1,
                                            bgcolor:"rgba(79,70,229,0.08)",
                                            color:"#4f46e5",
                                            fontWeight: 700
                                        }}
                                    />
                                )}
                            </Box>
                        </CardContent>
                    </Card>
                ))}
            </Box>
            {/* ================= FIRST LOADING ================= */}
            {loading && courses.length === 0
                && (
                    <Box
                        sx={{
                            display:"flex",
                            justifyContent: "center",
                            py: 8
                        }}
                    >
                        <CircularProgress />
                    </Box>
                )}
            {/* ================= LOAD MORE ================= */}
            {page > 0 && courses.length > 0
                && (
                    <Box
                        sx={{
                            display:"flex",
                            justifyContent: "center",
                            mt: 5
                        }}
                    >
                        <Button
                            variant="outlined"
                            disabled={loading}
                            onClick={loadMore}
                            sx={{
                                px:4,
                                py:1.2,
                                borderRadius:3,
                                textTransform:"none",
                                fontWeight:700
                            }}
                        >
                            {loading? (<><CircularProgress size={18} sx={{mr:1}}/>Đang tải...</>): "Xem thêm khóa học"}
                        </Button>
                    </Box>
                )}
            {/* ================= HẾT COURSE ================= */}
            {page === 0 && courses.length > 0
                && (
                    <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{
                            textAlign:"center",
                            mt: 4
                        }}
                    >
                        Bạn đã xem hết các khóa học.
                    </Typography>
                )}
            {/* ================= EMPTY ================= */}
            {!loading && courses.length === 0
                && (
                    <Box
                        sx={{
                            py: 8,
                            textAlign:"center"
                        }}
                    >
                        <SearchRoundedIcon
                            sx={{
                                fontSize:50,
                                color:"#94a3b8",
                                mb:1
                            }}
                        />
                        <Typography
                            variant="h6"
                            fontWeight={700}
                        >
                            Không tìm thấy khóa học
                        </Typography>
                        <Typography color="text.secondary">
                            Hãy thử tìm kiếm bằng từ khóa khác.
                        </Typography>
                    </Box>
                )}
        </Box>
    );
};
export default CoursesScreen;