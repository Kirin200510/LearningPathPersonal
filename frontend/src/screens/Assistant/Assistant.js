import { useEffect, useRef, useState } from "react";
import {Avatar,Box,IconButton,Paper,TextField,Typography,CircularProgress,Button} from "@mui/material";
import SmartToyRoundedIcon from "@mui/icons-material/SmartToyRounded";
import SendRoundedIcon from "@mui/icons-material/SendRounded";
import PersonRoundedIcon from "@mui/icons-material/PersonRounded";
import {authApis,endpoints} from "../../configs/Apis";


const Assistant = () => {
    const [loading, setLoading] = useState(false);
    const DEFAULT_MESSAGES = [
    {
        role: "bot",
        content: "Xin chào! Tôi là trợ lý học tập của bạn. Tôi có thể giúp gì cho bạn hôm nay?"
    }
    ];
    //load trang không bị mất đoạn chat cũ
    const [messages, setMessages] = useState(() => {
        const savedMessages = localStorage.getItem("assistant_messages");
        if (savedMessages) {
            try {
                return JSON.parse(savedMessages)
            } catch (ex) {
                console.log(ex)
            }
        }
        return DEFAULT_MESSAGES
    });
    const sessionId=useRef(localStorage.getItem("assistant_session_id") || `session-${Date.now()}`)
    useEffect(()=>{
        localStorage.setItem('assistant_session_id',sessionId.current);
    },[]);
    useEffect(()=>{
        localStorage.setItem("assistant_messages",JSON.stringify(messages))
    },[messages]);


    const [input, setInput] = useState("");
    const messagesEndRef = useRef(null);
    // giúp chuyển tab vô lại không mất selected_program
    const [selectedProgramId,setSelectedProgramId] = useState(()=>{
        return localStorage.getItem("assistant_selected_program_id") || null;
    });

    useEffect(() => {
        if (selectedProgramId) {
            localStorage.setItem(
            "assistant_selected_program_id",
            selectedProgramId
            );
        } else {
            localStorage.removeItem(
            "assistant_selected_program_id"
            );
        }
    }, [selectedProgramId]);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSend = async (e) => {
        e.preventDefault(); // ngăn reload
        if (!input.trim() || loading) return;

        const userMessage = {
            role: "user",
            content: input
        };
        setMessages(prev => [...prev, userMessage]);
        setInput("");
        setLoading(true);

        // Gọi API RAG
        try {
            const token = localStorage.getItem("token");
            let res = await authApis(token).post(endpoints["rag-ask"], {
                query: userMessage.content,
                session_id: sessionId.current
            });
            const botMessage = {
                role: "bot",
                content: res.data.answer
            };
            setMessages(prev => [...prev, botMessage]);
            setSelectedProgramId(res.data.selected_program_id || null);
        } catch (error) {
            console.error("RAG Error", error);
        } finally {
            setLoading(false);
        }
    };

    const handleProgramDecision = async (action) => {
        if (loading) return;
        try{
            setLoading(true);
            const userDecision = {
                role: "user",
                content:
                    action === "confirm"
                        ? "Tôi xác nhận lộ trình này."
                        : "Tôi từ chối lộ trình này."
            };
            setMessages(prev => [...prev,userDecision]);

            const token = localStorage.getItem("token");
            let res = await authApis(token).post(endpoints["program-decision"], {
                session_id: sessionId.current,
                action: action
            });
            const botMessage = {
                role: "bot",
                content: res.data.answer
            };
            setMessages(prev => [...prev, botMessage]);
            setSelectedProgramId(null);

        } catch (error) {
            console.error("Program Decision Error", error);
        } finally {
            setLoading(false);
        }
    };

    const handleNewChat=() => {
        const newSessionId= `session-${Date.now()}`;
        sessionId.current=newSessionId;
        localStorage.setItem("assistant_session_id",newSessionId);
        setMessages(DEFAULT_MESSAGES);
        localStorage.removeItem('assistant_messages');
        setSelectedProgramId(null);
        setInput("");
    };

    return (
        <Box
            sx={{
                height: "100vh",
                p: {
                    xs: 2,
                    md: 4
                },
                display: "flex",
                flexDirection: "column",
                bgcolor: "#f8fafc"
            }}>
            <Box
            sx={{
                mb: 3,
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                gap: 2
            }}>
            {/* Bên trái: tiêu đề */}
            <Box
                sx={{
                    display: "flex",
                    alignItems: "center",
                    gap: 1.5
                }}
            >
                <Box
                    sx={{
                        width: 44,
                        height: 44,
                        borderRadius: 2.5,
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        color: "white",
                        background:
                            "linear-gradient(135deg, #6366f1, #10b981)",
                        boxShadow:
                            "0 8px 20px rgba(99,102,241,0.20)"
                    }}
                >
                    <SmartToyRoundedIcon />
                </Box>

                <Box>
                    <Typography
                        variant="h4"
                        fontWeight={800}
                        sx={{ color: "#0f172a" }}
                    >
                        AI Assistant
                    </Typography>

                    <Typography
                        variant="body2"
                        color="text.secondary"
                    >
                        Trợ lý học tập và định hướng nghề nghiệp
                    </Typography>
                </Box>
            </Box>


            {/* Bên phải: New Chat */}
            <Button
                variant="outlined"
                onClick={handleNewChat}
                disabled={loading}
                sx={{
                    borderRadius: 2.5,
                    px: 2,
                    py: 1,
                    textTransform: "none",
                    fontWeight: 700
                }}
            >
                Đoạn chat mới
            </Button>
        </Box>
            {/* Chat container */}
            <Paper
                elevation={0}
                sx={{
                    flexGrow: 1,
                    display: "flex",
                    flexDirection: "column",
                    minHeight: 0,
                    overflow: "hidden",
                    borderRadius: 4,
                    border:"1px solid #e5e7eb",
                    boxShadow:"0 8px 30px rgba(15,23,42,0.06)"
                }}
            >
                {/* Chat top bar */}
                <Box
                    sx={{
                        px: 3,
                        py: 2,
                        display: "flex",
                        alignItems: "center",
                        gap: 1.5,
                        bgcolor: "white",
                        borderBottom:"1px solid #e5e7eb"
                    }}
                >
                    <Avatar
                        sx={{
                            width: 38,
                            height: 38,
                            background:"linear-gradient(135deg, #6366f1, #818cf8)"
                        }}>
                        <SmartToyRoundedIcon fontSize="small"/>
                    </Avatar>
                    <Box>
                        <Typography fontWeight={700}>
                            LearningPath AI
                        </Typography>
                        <Typography
                            variant="caption"
                            sx={{
                                color: "#10b981"
                            }}>
                            Sẵn sàng hỗ trợ
                        </Typography>
                    </Box>
                </Box>
                {/* Messages */}
                <Box
                    sx={{
                        flexGrow: 1,
                        minHeight: 0,
                        overflowY: "auto",
                        p: 3,
                        display: "flex",
                        flexDirection: "column",
                        gap: 2.5,
                        background: "linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%)"
                    }}
                >
                    {messages.map(
                        (message, index) => {
                            const isUser =
                                message.role ===
                                "user";
                            return (
                                <Box
                                    key={index}
                                    sx={{
                                        display: "flex",
                                        justifyContent:isUser? "flex-end" : "flex-start",
                                        alignItems:"flex-start",
                                        gap: 1.2
                                    }}
                                >
                                    {/* Bot avatar */}
                                    {!isUser && (
                                        <Avatar
                                            sx={{
                                                width: 34,
                                                height: 34,
                                                bgcolor: "#6366f1"
                                            }}
                                        >
                                            <SmartToyRoundedIcon
                                                sx={{fontSize: 19}}
                                            />
                                        </Avatar>

                                    )}
                                    {/* Bubble */}
                                    <Box
                                        sx={{
                                            maxWidth: {
                                                xs: "85%",
                                                md: "70%"
                                            },
                                            px: 2,
                                            py: 1.5,
                                            borderRadius: 3,
                                            bgcolor:isUser? "#4f46e5": "white",
                                            color:isUser? "white": "#1e293b",
                                            border:isUser? "none": "1px solid #e5e7eb",
                                            boxShadow:"0 3px 10px rgba(15,23,42,0.05)",
                                            borderTopRightRadius:isUser ? 6: 18,
                                            borderTopLeftRadius:isUser? 18: 6
                                        }}
                                    >
                                        <Typography
                                            variant="body1"
                                            sx={{
                                                lineHeight:1.7,
                                                whiteSpace: "pre-wrap"
                                            }}
                                        >
                                            {message.content}
                                        </Typography>

                                    </Box>


                                    {/* User avatar */}
                                    {isUser && (
                                        <Avatar
                                            sx={{
                                                width: 34,
                                                height: 34,
                                                bgcolor:"#10b981"
                                            }}>
                                            <PersonRoundedIcon
                                                sx={{fontSize: 19}}
                                            />
                                        </Avatar>
                                    )}
                                </Box>
                            );
                        }
                    )}
                    {selectedProgramId && !loading && (
                    <Box
                        sx={{
                            display: "flex",
                            justifyContent: "flex-start",
                            gap: 1.5,
                            pl: 5.5
                        }}>
                        <Button
                            variant="contained"
                            onClick={() =>handleProgramDecision("confirm")}
                            sx={{
                                borderRadius: 3,
                                textTransform: "none",
                                fontWeight: 700
                            }}
                        >
                            Xác nhận lộ trình
                        </Button>
                        <Button
                            variant="outlined"
                            onClick={() =>
                                handleProgramDecision("reject")}
                            sx={{
                                borderRadius: 3,
                                textTransform: "none",
                                fontWeight: 700
                            }}
                        >
                            Từ chối lộ trình
                        </Button>
                    </Box>
                )}
                    {loading && (
                    <Box
                        sx={{
                            display: "flex",
                            justifyContent: "flex-start",
                            alignItems: "flex-start",
                            gap: 1.2
                        }}>
                        <Avatar
                            sx={{
                                width: 34,
                                height: 34,
                                bgcolor: "#6366f1"
                            }}>
                            <SmartToyRoundedIcon sx={{ fontSize: 19 }}/>
                        </Avatar>
                        <Box
                            sx={{
                                px: 2,
                                py: 1.5,
                                bgcolor: "white",
                                border:"1px solid #e5e7eb",
                                borderRadius: 3,
                                borderTopLeftRadius: 6,
                                boxShadow:"0 3px 10px rgba(15,23,42,0.05)"
                            }}>
                            <CircularProgress size={20}/>
                        </Box>
                    </Box>

                )}
                <div ref={messagesEndRef}/>
                </Box>
                {/* Input */}
                <Box
                    component="form"
                    onSubmit={handleSend}
                    sx={{
                        p: 2,
                        display: "flex",
                        alignItems: "center",
                        gap: 1.5,
                        bgcolor: "white",
                        borderTop:"1px solid #e5e7eb"
                    }}
                >
                    <TextField
                        fullWidth
                        value={input}
                        onChange={(e) =>
                            setInput(
                                e.target.value
                            )
                        }
                        disabled={loading}
                        placeholder= "Ví dụ: Tôi muốn trở thành Backend Developer..."
                        size="small"
                        sx={{"& .MuiOutlinedInput-root":
                                {
                                    borderRadius: 3,
                                    bgcolor: "#f8fafc"
                                }
                        }}
                    />
                    <IconButton
                        type="submit"
                        disabled={!input.trim()}
                        sx={{
                            width: 44,
                            height: 44,
                            bgcolor:"primary.main",
                            color: "white",
                            "&:hover": {
                                bgcolor:"primary.dark"
                            },
                            "&.Mui-disabled": {
                                bgcolor:"#e2e8f0"
                            }
                        }}
                    >
                        <SendRoundedIcon />
                    </IconButton>
                </Box>
            </Paper>
        </Box>
    )
};
export default Assistant;


