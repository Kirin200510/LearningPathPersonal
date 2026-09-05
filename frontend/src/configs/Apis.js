import axios from "axios";

export const BASE_URL = process.env.REACT_APP_BASE_URL;
export const endpoints = {
    "login": "/token/",
    "register": "/users/",
    "current-user": "/users/me/",
    "rag-ask": "/rag/ask/",
    "program-decision": "rag/program-decision/",
    "courses": "/courses/",
    "learning-paths": "/learning_path/me/",
    "schedules": "/schedules/me",
    "profile": "/users/me/",
    "change-password": "/users/me/change-password/",

};
export const scheduleUpdateEndpoint = id =>
  `/schedules/me/${id}/`;

export const learningPathNodesEndpoint = (pathId) =>
    `/learning_path/${pathId}/nodes/`;

export const learningPathDeleteEndpoint = id =>
  `/learning_path/${id}/`;

// Hàm tạo axios instance có token để gọi các API cần xác thực
export const authApi = (token) => {
    return axios.create({
        baseURL: BASE_URL,
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
};

export const authApis = authApi;

// Axios instance mặc định
export default axios.create({
    baseURL: BASE_URL
});
