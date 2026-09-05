import { useEffect, useState } from "react";
import {Box, Typography, Paper, CircularProgress, Avatar, Divider,Button, Dialog, DialogTitle, DialogContent, DialogActions, Alert} from "@mui/material";
import RouteRoundedIcon from "@mui/icons-material/RouteRounded";
import {authApis,endpoints,learningPathNodesEndpoint,learningPathDeleteEndpoint} from "../../configs/Apis";
import AccessTimeRoundedIcon from "@mui/icons-material/AccessTimeRounded";
import DeleteOutlineRoundedIcon from "@mui/icons-material/DeleteOutlineRounded";

const LearningPath = () => {

    const [paths,setPaths] = useState([]);
    const [loading,setLoading] = useState(true);
    const [nodesByPath,setNodesByPath] = useState({});

    const [courses, setCourses] = useState({});
    const [coursePage, setCoursePage] = useState(1);
    const [courseLoading, setCourseLoading] = useState(false);

    const [expandedPaths, setExpandedPaths] = useState({});

    const [deleteOpen, setDeleteOpen] = useState(false);
    const [deletingPath, setDeletingPath] = useState(null);
    const [deleting, setDeleting] = useState(false);
    const [deleteError, setDeleteError] = useState("");

    const loadCourses = async () => {
        try {
            setCourseLoading(true);
            const token = localStorage.getItem("token");
            let url =`${endpoints["courses"]}?page=${coursePage}&size=60`;
            const response = await authApis(token).get(url);
            const newCourses = {};
            response.data.items.forEach(course => {
                newCourses[course.id] = course;
            });
            if (coursePage === 1) {
                setCourses(newCourses);
            } else if (coursePage > 1) {
                setCourses(prev => ({ ...prev, ...newCourses }));
            }
            if (coursePage < response.data.pages) {
                setCoursePage(coursePage + 1);
            } else {
                setCoursePage(0);
            }
        } catch (error) {
            console.error("Error loading courses:", error);
        } finally {
            setCourseLoading(false);
        }
    };

    const fetchLearningPath = async () => {
        try {
            const token = localStorage.getItem("token");
            const responses = await authApis(token).get(endpoints['learning-paths']);

            const userPaths=responses.data;
            setPaths(userPaths);

            const allNodes = {};
            for (const path of userPaths) {
                //DS nodes của path
                const nodesResponse = await authApis(token).get(learningPathNodesEndpoint(path.id));
                const sortedNodes = nodesResponse.data.sort((a, b) => a.sequence_order - b.sequence_order);
                allNodes[path.id] = sortedNodes;
            }
            setNodesByPath(allNodes);
        } catch (error) {
            console.error("Error fetching learning paths:", error);
        } finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        fetchLearningPath();
    }, []);

    useEffect(() => {
        const timer=setTimeout(() => {
            if (coursePage > 0 ) {
                loadCourses();
            }
        }, 1000);
        return () => clearTimeout(timer);
       
    }, [coursePage]);

    const handleOpenDelete = path => {
        setDeletingPath(path);
        setDeleteError("");
        setDeleteOpen(true);
    };

    const handleCloseDelete = () => {
        if (deleting) return;
        setDeleteOpen(false);
        setDeletingPath(null);
        setDeleteError("");
    };

    const handleDeletePath = async () => {
        if (!deletingPath) return;

        try {
            setDeleting(true);
            setDeleteError("");

            const token = localStorage.getItem("token");
            await authApis(token).delete(learningPathDeleteEndpoint(deletingPath.id));

            const deletedId = deletingPath.id;
            //lấy lộ trình khác trừ cái xóa ra frontend
            setPaths(prev => prev.filter(path => path.id !== deletedId));
            setNodesByPath(prev => {
                const next = { ...prev };
                delete next[deletedId];
                return next;
            });

            setExpandedPaths(prev => {
                const next = { ...prev };
                delete next[deletedId];
                return next;
            });

            setDeleteOpen(false);
            setDeletingPath(null);

        } catch (error) {
            console.error("Error deleting learning path:", error);

            if (error.response?.status === 404) {
                setDeleteError("Không tìm thấy lộ trình này.");
            } else {
                setDeleteError("Không thể xóa lộ trình. Vui lòng thử lại.");
            }
        } finally {
            setDeleting(false);
        }
    };

    return (
        <Box
            sx={{
                minHeight: "100vh",
                bgcolor: "#f8fafc",
                p: {xs: 2,md: 4}
            }}
        >
            {/* ================= HEADER ================= */}
            <Box sx={{ mb: 4 }}>
                <Box
                    sx={{
                        display: "flex",
                        alignItems: "center",
                        gap: 1.5
                    }}>
                    {/* Icon */}
                    <Box
                        sx={{
                            width: 44,
                            height: 44,
                            borderRadius: 2.5,
                            display: "flex",
                            justifyContent:"center",
                            alignItems:"center",
                            color: "white",
                            background:"linear-gradient(135deg, #6366f1, #10b981)",
                            boxShadow:"0 8px 20px rgba(99, 102, 241, 0.20)"
                        }}>
                        <RouteRoundedIcon />
                    </Box>
                    {/* Tiêu đề */}
                    <Box>
                        <Typography
                            variant="h4"
                            fontWeight={800}
                            sx={{color: "#0f172a"}}>
                            Learning Path
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            Các lộ trình học tập của bạn
                        </Typography>
                    </Box>
                </Box>
            </Box>
            {/* ================= LOADING ================= */}
            {loading ? (
                <Box
                    sx={{
                        minHeight: 350,
                        display: "flex",
                        justifyContent:"center",
                        alignItems:"center"
                    }}>
                    <CircularProgress />
                </Box>
            ) : paths.length > 0 ? (
                /* ================= CÓ LEARNING PATH ================= */
                <Box
                    sx={{
                        display: "flex",
                        flexDirection:"column",
                        gap: 3
                    }}>
                    {paths.map((path, pathIndex) => {
                            // Lấy node thuộc path hiện tại
                            const pathNodes = nodesByPath[path.id] || [];
                            const isExpanded = expandedPaths[path.id] || false;
                            const visibleNodes = isExpanded ? pathNodes: pathNodes.slice(0, 10);
                            return (
                                <Paper
                                    key={path.id}
                                    elevation={0}
                                    sx={{
                                        borderRadius: 4,
                                        overflow: "hidden",
                                        border:"1px solid #e5e7eb",
                                        boxShadow:"0 8px 30px rgba(15, 23, 42, 0.06)",
                                        bgcolor:"white"
                                    }}>
                                    {/* ========== THÔNG TIN PATH ========== */}
                                    <Box
                                        sx={{
                                            px: {xs: 2, md: 3},
                                            py: 2.5,
                                            borderBottom:"1px solid #e5e7eb",
                                            background:"linear-gradient(135deg, rgba(99,102,241,0.06), rgba(16,185,129,0.04))",
                                            display: "flex",
                                            justifyContent:"space-between",
                                            alignItems: "center",
                                            gap: 2
                                        }}>
                                        <Box>
                                            <Typography
                                                variant="h6"
                                                fontWeight={800}
                                                color="#0f172a">
                                                Learning Path #{path.id}
                                            </Typography>
                                            <Typography
                                                variant="body2"
                                                color="text.secondary"
                                                sx={{mt: 0.5 }}
                                            >
                                                Ngày tạo:{" "}{new Date(path.created_at).toLocaleDateString("vi-VN")}
                                            </Typography>
                                            {path.url && (
                                                <Typography
                                                    component="a"
                                                    href={path.url}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    variant="body2"
                                                    sx={{
                                                        display: "block",
                                                        mt: 0.7,
                                                        color: "#6366f1",
                                                        textDecoration: "none",
                                                        width: "fit-content",
                                                        "&:hover": {textDecoration: "underline"}
                                                    }}
                                                >
                                                    Link lộ trình:{path.url}
                                                </Typography>
                                            )}
                                        </Box>
                                        <Box sx={{ display: "flex", alignItems: "center", gap: 1.5 }}>
                                            {pathIndex === 0 && (
                                                <Box sx={{
                                                px: 1.5, py: 0.6, borderRadius: 2,
                                                bgcolor: "rgba(16,185,129,0.10)",
                                                color: "#059669", fontSize: 13, fontWeight: 700
                                                }}>
                                                Mới nhất
                                                </Box>
                                            )}

                                            <Button
                                                variant="outlined"
                                                color="error"
                                                size="small"
                                                startIcon={<DeleteOutlineRoundedIcon />}
                                                onClick={() => handleOpenDelete(path)}
                                                sx={{
                                                borderRadius: 2.5,
                                                textTransform: "none",
                                                fontWeight: 700
                                                }}
                                            >
                                                Xóa lộ trình
                                            </Button>
                                        </Box>
                                    </Box>
                                    {/* ========== DANH SÁCH COURSE ========== */}
                                    <Box>
                                        {pathNodes.length > 0 ? (visibleNodes.map((node,index) => {
                                            // Tìm Course bằng course_id
                                            const course =courses[ node.course_id ];
                                            return (<Box key={node.id}>
                                                        <Box
                                                            sx={{display:"flex",
                                                                gap: 2,
                                                                px: { xs: 2,md: 3},
                                                                py: 3,
                                                                alignItems:"flex-start",
                                                                transition:"0.2s",
                                                                "&:hover":{bgcolor:"#f8fafc"}
                                                                }}
                                                            >
                                                                {/* SỐ THỨ TỰ */}
                                                                <Avatar
                                                                    sx={{
                                                                        width: 44,
                                                                        height: 44,
                                                                        bgcolor:"#6366f1",
                                                                        fontWeight:800,
                                                                        boxShadow:"0 6px 18px rgba(99,102,241,0.20)"
                                                                    }}>

                                                                    {node.sequence_order}
                                                                </Avatar>
                                                                {/* THÔNG TIN COURSE */}
                                                                <Box
                                                                    sx={{
                                                                        flex: 1,
                                                                        minWidth: 0
                                                                    }}
                                                                >

                                                                    {/* Tên Course */}

                                                                    <Typography
                                                                        variant="h6"
                                                                        fontWeight={800}
                                                                        sx={{
                                                                            color:"#0f172a",
                                                                            mb: 0.75
                                                                        }}
                                                                    >

                                                                        {course? course.title: `Course #${node.course_id}`}
                                                                    </Typography>
                                                                    {/* Số giờ */}
                                                                    {Number(course?.estimated_hours) > 0 && (
                                                                        <Box sx={{
                                                                            display:"flex",
                                                                            alignItems:"center",
                                                                            gap: 0.5,
                                                                            mb: 1
                                                                            }}>
                                                                            <AccessTimeRoundedIcon sx={{fontSize: 18,color:"#64748b"}}/>
                                                                            <Typography
                                                                                variant="body2"
                                                                                color="text.secondary"
                                                                                fontWeight={600}
                                                                                >
                                                                                    {course.estimated_hours}{" "}giờ
                                                                                </Typography>
                                                                            </Box>
                                                                        )}
                                                                    {/* Mô tả Course */}
                                                                    {course && course.description && (
                                                                        <Typography
                                                                            variant="body2"
                                                                            color="text.secondary"
                                                                            sx={{ lineHeight: 1.7,maxWidth: 850}}
                                                                            >
                                                                            {course.description}
                                                                        </Typography>
                                                                        )}
                                                                </Box>
                                                            </Box>
                                                            {/* Đường phân cách */}
                                                            {index < visibleNodes.length - 1 && (<Divider />)}
                                                        </Box>
                                                    );
                                                }
                                            )
                                        ) : (
                                            /* Path không có Course */
                                            <Box
                                                sx={{
                                                    textAlign: "center",
                                                    py: 5,
                                                    px: 2
                                                }}
                                            >
                                                <Typography variant="body2" color="text.secondary">
                                                    Learning Path này chưa có khóa học nào.
                                                </Typography>
                                            </Box>
                                        )}
                                        {/* Nút Xem thêm / Thu gọn */}
                                        {pathNodes.length > 10 && (
                                        <Box
                                            sx={{
                                                display: "flex",
                                                justifyContent:"center",
                                                py: 2,
                                                borderTop:"1px solid #e5e7eb"
                                            }}
                                        >
                                            <Typography
                                                component="button"
                                                onClick={() => {
                                                    setExpandedPaths((prev) => ({ ...prev,[path.id]:!prev[path.id]}));
                                                }}
                                                sx={{
                                                    border: "none",
                                                    background:"transparent",
                                                    color: "#6366f1",
                                                    fontWeight:700,
                                                    cursor:"pointer",
                                                    fontSize:14,
                                                    "&:hover": { textDecoration:"underline"}
                                                }}
                                            >
                                                {isExpanded? "Thu gọn": `Hiển thị tất cả (${pathNodes.length} khóa học)`}
                                            </Typography>
                                        </Box>
                                    )}
                                    </Box>
                                </Paper>
                            );
                        }
                    )}
                </Box>
            ) : (
                /* ================= KHÔNG CÓ LEARNING PATH ================= */
                <Paper
                    elevation={0}
                    sx={{
                        textAlign: "center",
                        py: {
                            xs: 6,
                            md: 8
                        },
                        px: 3,
                        borderRadius: 4,
                        border:"1px solid #e5e7eb",
                        boxShadow: "0 8px 30px rgba(15,23,42,0.06)",
                        bgcolor: "white"
                    }}
                >
                    {/* Icon */}
                    <Box
                        sx={{
                            width: 64,
                            height: 64,
                            borderRadius: 3,
                            mx: "auto",
                            mb: 2,
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            color:"#6366f1",
                            bgcolor:"rgba(99,102,241,0.08)"
                        }}
                    >
                        <RouteRoundedIcon
                            sx={{fontSize: 34}}
                        />
                    </Box>
                    <Typography
                        variant="h5"
                        fontWeight={800}
                        sx={{mb: 1}}
                    >
                        Chưa có Learning Path
                    </Typography>
                    <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{
                            maxWidth: 500,
                            mx: "auto",
                            lineHeight: 1.7
                        }}
                    >
                        Hãy sử dụng AI Assistant để nhận gợi ý
                        chương trình học và tạo lộ trình phù hợp
                        với mục tiêu của bạn.
                    </Typography>
                </Paper>
            )}
        <Dialog open={deleteOpen} onClose={handleCloseDelete} fullWidth maxWidth="xs">
            <DialogTitle fontWeight={800}>
                Xóa lộ trình?
            </DialogTitle>

            <DialogContent>
                {deleteError && (
                <Alert severity="error" sx={{ mb: 2 }}>
                    {deleteError}
                </Alert>
                )}

                <Typography>
                Bạn có chắc muốn xóa{" "}
                <strong>Learning Path #{deletingPath?.id}</strong>?
                </Typography>

                <Typography variant="body2" color="text.secondary" sx={{ mt: 1.5, lineHeight: 1.7 }}>
                Toàn bộ lịch học thuộc lộ trình này cũng sẽ bị xóa.
                Các khóa học trong danh mục sẽ không bị ảnh hưởng.
                </Typography>
            </DialogContent>

            <DialogActions sx={{ px: 3, pb: 3 }}>
                <Button
                onClick={handleCloseDelete}
                disabled={deleting}
                sx={{ textTransform: "none" }}
                >
                Hủy
                </Button>

                <Button
                variant="contained"
                color="error"
                disabled={deleting}
                onClick={handleDeletePath}
                startIcon={!deleting && <DeleteOutlineRoundedIcon />}
                sx={{ borderRadius: 2.5, textTransform: "none", fontWeight: 700 }}
                >
                {deleting ? (
                    <>
                    <CircularProgress size={17} color="inherit" sx={{ mr: 1 }} />
                    Đang xóa...
                    </>
                ) : (
                    "Xóa lộ trình"
                )}
                </Button>
            </DialogActions>
        </Dialog>
        </Box>
        
    );
};
export default LearningPath;
