import React, { useEffect, useState } from "react";
import {
  Alert, Box, Button, Card, Chip, CircularProgress, Dialog, DialogActions,
  DialogContent, DialogTitle, IconButton, Paper, Switch, Table, TableBody,
  TableCell, TableContainer, TableHead, TableRow, TextField, Tooltip, Typography,Pagination
} from "@mui/material";
import EventIcon from "@mui/icons-material/Event";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import EditRoundedIcon from "@mui/icons-material/EditRounded";
import CalendarMonthRoundedIcon from "@mui/icons-material/CalendarMonthRounded";
import NotificationsActiveRoundedIcon from "@mui/icons-material/NotificationsActiveRounded";
import NotificationsOffRoundedIcon from "@mui/icons-material/NotificationsOffRounded";
import { authApis, endpoints, scheduleUpdateEndpoint } from "../../configs/Apis";

const Schedule = () => {
    const [schedules,setSchedules]=useState([]);
    const [courses,setCourses]=useState({});
    const [loading,setLoading]=useState(false);
    const [error, setError] = useState("");
    const [saving, setSaving] = useState(false);

    const [editOpen, setEditOpen] = useState(false);
    const [editingSchedule, setEditingSchedule] = useState(null);
    const [editForm,setEditForm]=useState({
        schedule_date:"",
        start_time: "",
        end_time: "",
        is_reminder_enabled: true
    });

    const [learningPaths, setLearningPaths] = useState([]);
    const [pathPage, setPathPage] = useState(1);

    const loadLearningPaths = async () => {
        const token = localStorage.getItem("token");
        const res = await authApis(token).get(endpoints["learning-paths"]);
        setLearningPaths(res.data || []);
    };

    const loadCourses = async () => {
        const token = localStorage.getItem("token");
        let page = 1;
        const dict = {};
        while (page > 0) {
            const res = await authApis(token).get(`${endpoints["courses"]}?page=${page}&size=100`);
            (res.data.items || []).forEach(course => {
                dict[course.id] = course;
            });

            if (page < res.data.pages) page += 1;
            else page = 0;
        }
        setCourses(dict);
    };
    
    const loadSchedules=async()=> {
        const token = localStorage.getItem("token");
        const res = await authApis(token).get(endpoints["schedules"]);
        const sortedTime=[...res.data].sort((a,b)=>{
            const timeA=new Date(`${a.schedule_date}T${a.start_time}`);
            const timeB=new Date(`${b.schedule_date}T${b.start_time}`);
            return timeB-timeB
        });
        setSchedules(sortedTime)
    };
    const fetchData= async() => {
        try {
            setLoading(true);
            await Promise.all([loadSchedules(), loadCourses(),loadLearningPaths()]);
        } catch (err) {
            console.error("Error loading schedules:", err);
        } finally {
            setLoading(false);
        }
    };
    useEffect(()=>{
        fetchData();
    },[]);
    const formatDate = value => {
        if (!value) return "";
        const [year, month, day] = value.split("-");
        return `${day}/${month}/${year}`;
    };

    const formatTime = value => value ? value.slice(0, 5) : "";

    const isSchedulePast = schedule => {
        const end = new Date(`${schedule.scheduled_date}T${schedule.end_time}`);
        return end < new Date();
    };

    const handleOpenEdit = schedule =>{
        setSaving(false);
        setEditingSchedule(schedule);
        setEditForm({
            scheduled_date: schedule.scheduled_date,
            start_time: formatTime(schedule.start_time),
            end_time: formatTime(schedule.end_time),
            is_reminder_enabled: Boolean(schedule.is_reminder_enabled)
        });
        setEditOpen(true);
    };

    const handleCloseEdit = () =>{
        if (saving) return;
        setEditOpen(false);
        setEditingSchedule(null);
    };

    const handleEditChange = e => {
        const { name, value } = e.target;
        setEditForm(prev => ({ ...prev, [name]: value }));
    };

    const handleUpdateSchedule = async() => {
        if (!editingSchedule) return;
        if (!editForm.scheduled_date || !editForm.start_time || !editForm.end_time) {
            setError("Vui lòng nhập đầy đủ ngày và thời gian.");
            return;
        }
        if (editForm.start_time >= editForm.end_time) {
            setError("Giờ bắt đầu phải trước giờ kết thúc.");
            return;
        }
        try {
            setSaving(true);
            setError("");
            const token = localStorage.getItem("token");

            await authApis(token).patch(
                scheduleUpdateEndpoint(editingSchedule.id),
                {
                scheduled_date: editForm.scheduled_date,
                start_time: editForm.start_time,
                end_time: editForm.end_time,
                is_reminder_enabled: editForm.is_reminder_enabled
                }
            );
            await loadSchedules();
            setEditOpen(false);
            setEditingSchedule(null);
        } catch (ex) {
            console.error(ex)
        } finally {
            setSaving(false);
        }
    };
    //Lấy schedule theo learningpath
    const currentPath = learningPaths[pathPage - 1];
    const currentSchedules = currentPath? schedules.filter(schedule => schedule.learning_path_id === currentPath.id): [];

    const [reminderOpen, setReminderOpen] = useState(false);
    const [reminderSchedule, setReminderSchedule] = useState(null);

    //Nhắc lịch gần nhất theo lộ trình
    const getNearestReminder = schedules => {
        const now = new Date();
        const scheduleReminders=schedules.filter(schedule => {
            if (schedule.is_reminder_enabled===false) {
                return false;
            }
            const startDateTime = `${schedule.scheduled_date}T${schedule.start_time}`;
            const startTime = new Date(startDateTime);
            if (startTime <= now) {
                return false;
            } 
            return true;
        });
        scheduleReminders.sort((scheduleA,scheduleB)=>{
            const startTimeA = new Date(`${scheduleA.scheduled_date}T${scheduleA.start_time}`);
            const startTimeB = new Date(`${scheduleB.scheduled_date}T${scheduleB.start_time}`);
            return startTimeA - startTimeB;
        });

        if (scheduleReminders.length===0) return null;
        return scheduleReminders[0];
    };

    const shouldShowReminder = schedule => {
        if (!schedule) return false;

        const now = new Date();
        const startTime = new Date(
            `${schedule.scheduled_date}T${schedule.start_time}`
        );

        const hoursLeft = (startTime - now) / (1000 * 60 * 60);
        return hoursLeft > 0 && hoursLeft <= 24;
    };
    useEffect(()=>{
        if(loading||schedules.length===0) return;
        const nearest=getNearestReminder(schedules);
        if (!nearest || !shouldShowReminder(nearest)) return;
        const reminderKey = `${nearest.id}-${nearest.scheduled_date}-${nearest.start_time}`;
        // lấy id nhắc lịch bộ nhớ của tab trình duyệt hiện tại
        const reminded =sessionStorage.getItem("last_reminded_schedule");
        //nếu chạy nhắc lịch rồi thì không nhắc nữa
        if (reminded===reminderKey) return;
        //chưa nhắc
        setReminderSchedule(nearest);
        setReminderOpen(true);
        sessionStorage.setItem("last_reminded_schedule", reminderKey);
    },[loading,schedules]);

    const reminderCourse = reminderSchedule?courses[reminderSchedule.course_id]: null;
    const reminderPathIndex = reminderSchedule? learningPaths.findIndex(path => path.id === reminderSchedule.learning_path_id): -1;
    const reminderPathNumber = reminderPathIndex >= 0 ? reminderPathIndex + 1 : null;

    return (
    <Box sx={{ p: { xs: 2, md: 4 }, minHeight: "100vh", bgcolor: "#f8fafc" }}>
      {/* HEADER */}
      <Box sx={{ display: "flex", alignItems: "center", gap: 1.5, mb: 4 }}>
        <Box sx={{
          width: 46, height: 46, borderRadius: 2.5,
          display: "flex", alignItems: "center", justifyContent: "center",
          color: "white",
          background: "linear-gradient(135deg, #4f46e5, #10b981)",
          boxShadow: "0 8px 20px rgba(79,70,229,0.20)"
        }}>
          <CalendarMonthRoundedIcon />
        </Box>

        <Box>
          <Typography
            variant="h4"
            fontWeight={800}
            sx={{
              background: "linear-gradient(135deg, #4f46e5, #10b981)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent"
            }}
          >
            Personal Schedule
          </Typography>

          <Typography variant="body1" color="text.secondary">
            Quản lý lịch học được tạo từ lộ trình của bạn.
          </Typography>
        </Box>
      </Box>

      {error && !editOpen && (
        <Alert severity="error" onClose={() => setError("")} sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
    {currentPath && (
        <Box sx={{
            mb: 2,
            p: 2.5,
            borderRadius: 3,
            bgcolor: "white",
            border: "1px solid #e5e7eb"
        }}>
            <Typography variant="h6" fontWeight={800} sx={{ color: "#0f172a" }}>
            Lộ trình {pathPage}
            </Typography>

            <Typography variant="body2" color="text.secondary">
            Lộ trình {pathPage} / {learningPaths.length}
            </Typography>
        </Box>
        )}
      {loading ? (
        <Box sx={{ minHeight: 350, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <CircularProgress />
        </Box>
      ) : (
        <Card
          elevation={0}
          sx={{
            borderRadius: 4,
            border: "1px solid #e5e7eb",
            overflow: "hidden",
            boxShadow: "0 8px 30px rgba(15,23,42,0.06)"
          }}
        >
          <TableContainer component={Paper} elevation={0}>
            <Table sx={{ minWidth: 850 }}>

              <TableHead sx={{ bgcolor: "rgba(79,70,229,0.05)" }}>
                <TableRow>
                  <TableCell>Ngày</TableCell>
                  <TableCell>Thời gian</TableCell>
                  <TableCell>Khóa học</TableCell>
                  <TableCell align="center">Trạng thái</TableCell>
                  <TableCell align="center">Nhắc lịch</TableCell>
                  <TableCell align="center">Cập nhật</TableCell>
                </TableRow>
              </TableHead>

              <TableBody>
                {currentSchedules.map(schedule => {
                  const course = courses[schedule.course_id];
                  const past = isSchedulePast(schedule);

                  return (
                    <TableRow
                      key={schedule.id}
                      hover
                      sx={{ opacity: past ? 0.65 : 1 }}
                    >
                      <TableCell>
                        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                          <EventIcon fontSize="small" sx={{ color: "#64748b" }} />
                          {formatDate(schedule.scheduled_date)}
                        </Box>
                      </TableCell>

                      <TableCell>
                        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                          <AccessTimeIcon fontSize="small" sx={{ color: "#64748b" }} />
                          {formatTime(schedule.start_time)} - {formatTime(schedule.end_time)}
                        </Box>
                      </TableCell>

                      <TableCell sx={{ fontWeight: 600 }}>
                        {course?.url ? (
                          <Box
                            component="a"
                            href={course.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            sx={{
                              color: "#4f46e5",
                              textDecoration: "none",
                              "&:hover": { textDecoration: "underline" }
                            }}
                          >
                            {course.title}
                          </Box>
                        ) : (
                          course?.title || `Course #${schedule.course_id}`
                        )}
                      </TableCell>

                      <TableCell align="center">
                        <Chip
                          size="small"
                          label={past ? "Completed" : "Upcoming"}
                          color={past ? "default" : "success"}
                          variant={past ? "outlined" : "filled"}
                        />
                      </TableCell>

                      <TableCell align="center">
                        {schedule.is_reminder_enabled ? (
                          <Chip
                            icon={<NotificationsActiveRoundedIcon />}
                            label="Đã bật"
                            size="small"
                            color="secondary"
                            variant="outlined"
                          />
                        ) : (
                          <Chip
                            icon={<NotificationsOffRoundedIcon />}
                            label="Đã tắt"
                            size="small"
                            variant="outlined"
                          />
                        )}
                      </TableCell>

                      <TableCell align="center">
                        <Tooltip title="Cập nhật lịch">
                          <IconButton
                            onClick={() => handleOpenEdit(schedule)}
                            sx={{
                              color: "#4f46e5",
                              bgcolor: "rgba(79,70,229,0.06)",
                              "&:hover": { bgcolor: "rgba(79,70,229,0.12)" }
                            }}
                          >
                            <EditRoundedIcon />
                          </IconButton>
                        </Tooltip>
                      </TableCell>
                    </TableRow>
                  );
                })}

                {currentSchedules.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={6} align="center" sx={{ py: 7 }}>
                      <CalendarMonthRoundedIcon sx={{ fontSize: 48, color: "#94a3b8", mb: 1 }} />

                      <Typography variant="h6" fontWeight={700}>
                        Chưa có lịch học
                      </Typography>

                      <Typography variant="body2" color="text.secondary">
                        Lịch học sẽ được tạo khi bạn xác nhận lộ trình với AI Assistant.
                      </Typography>
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>

            </Table>
          </TableContainer>
        </Card>
      )}
        {learningPaths.length > 1 && (
        <Box sx={{ display: "flex", justifyContent: "center", mt: 3 }}>
            <Pagination
            count={learningPaths.length}
            page={pathPage}
            onChange={(event, value) => setPathPage(value)}
            color="primary"
            shape="rounded"
            />
        </Box>
        )}

    {/* REMINDER DIALOG */}
    <Dialog
    open={reminderOpen}
    onClose={() => setReminderOpen(false)}
    fullWidth
    maxWidth="sm"
    >
    <DialogTitle fontWeight={800}>
        🔔 Nhắc lịch học
    </DialogTitle>

    <DialogContent>
        <Box
        sx={{
            mt: 1,
            p: 2.5,
            borderRadius: 3,
            bgcolor: "rgba(79,70,229,0.05)"
        }}
        >
        <Typography variant="body2" color="text.secondary">
            Buổi học sắp tới
        </Typography>

        {reminderPathNumber && (
            <Typography
            fontWeight={700}
            sx={{ color: "#4f46e5", mt: 1 }}
            >
            Lộ trình {reminderPathNumber}
            </Typography>
        )}

        <Typography variant="h6" fontWeight={800} sx={{ mt: 1 }}>
            {reminderCourse?.title ||
            `Course #${reminderSchedule?.course_id}`}
        </Typography>

        <Box sx={{ mt: 2, display: "flex", flexDirection: "column", gap: 1 }}>
            <Typography>
            Ngày: {formatDate(reminderSchedule?.scheduled_date)}
            </Typography>

            <Typography>
            Thời gian: {formatTime(reminderSchedule?.start_time)}
            {" - "}
            {formatTime(reminderSchedule?.end_time)}
            </Typography>
        </Box>
        </Box>
    </DialogContent>

    <DialogActions sx={{ px: 3, pb: 3 }}>
        <Button
        variant="contained"
        onClick={() => setReminderOpen(false)}
        sx={{
            borderRadius: 2.5,
            px: 3,
            textTransform: "none",
            fontWeight: 700
        }}
        >
        Đã hiểu
        </Button>
    </DialogActions>
    </Dialog>

      {/* UPDATE DIALOG */}
      <Dialog open={editOpen} onClose={handleCloseEdit} fullWidth maxWidth="sm">
        <DialogTitle fontWeight={800}>
          Cập nhật lịch học
        </DialogTitle>

        <DialogContent>
          {editingSchedule && (
            <Box sx={{ mb: 3, p: 2, borderRadius: 2.5, bgcolor: "rgba(79,70,229,0.05)" }}>
              <Typography variant="caption" color="text.secondary">
                Khóa học
              </Typography>

              <Typography fontWeight={700}>
                {courses[editingSchedule.course_id]?.title ||
                  `Course #${editingSchedule.course_id}`}
              </Typography>
            </Box>
          )}

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <TextField
            fullWidth
            type="date"
            label="Ngày học"
            name="scheduled_date"
            value={editForm.scheduled_date}
            onChange={handleEditChange}
            slotProps={{ inputLabel: { shrink: true } }}
            sx={{ mb: 2 }}
          />

          <Box sx={{
            display: "grid",
            gridTemplateColumns: { xs: "1fr", sm: "1fr 1fr" },
            gap: 2
          }}>
            <TextField
              fullWidth
              type="time"
              label="Giờ bắt đầu"
              name="start_time"
              value={editForm.start_time}
              onChange={handleEditChange}
              slotProps={{ inputLabel: { shrink: true } }}
            />

            <TextField
              fullWidth
              type="time"
              label="Giờ kết thúc"
              name="end_time"
              value={editForm.end_time}
              onChange={handleEditChange}
              slotProps={{ inputLabel: { shrink: true } }}
            />
          </Box>

          <Box sx={{
            mt: 3, p: 2, borderRadius: 2.5, bgcolor: "#f8fafc",
            display: "flex", justifyContent: "space-between", alignItems: "center"
          }}>
            <Box>
              <Typography fontWeight={700}>Nhắc lịch</Typography>
              <Typography variant="body2" color="text.secondary">
                Bật hoặc tắt nhắc lịch cho buổi học này.
              </Typography>
            </Box>

            <Switch
              checked={editForm.is_reminder_enabled}
              onChange={e =>
                setEditForm(prev => ({
                  ...prev,
                  is_reminder_enabled: e.target.checked
                }))
              }
              color="secondary"
            />
          </Box>
        </DialogContent>

        <DialogActions sx={{ px: 3, pb: 3 }}>
          <Button
            onClick={handleCloseEdit}
            disabled={saving}
            sx={{ textTransform: "none" }}
          >
            Hủy
          </Button>

          <Button
            variant="contained"
            onClick={handleUpdateSchedule}
            disabled={saving}
            sx={{
              px: 3,
              borderRadius: 2.5,
              textTransform: "none",
              fontWeight: 700,
              background: "linear-gradient(135deg, #4f46e5, #6366f1)"
            }}
          >
            {saving ? (
              <>
                <CircularProgress size={18} sx={{ mr: 1, color: "white" }} />
                Đang cập nhật...
              </>
            ) : (
              "Cập nhật lịch"
            )}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
    );
};
export default Schedule;