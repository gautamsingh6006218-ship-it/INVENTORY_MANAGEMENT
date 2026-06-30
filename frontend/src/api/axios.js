import axios from "axios";

// pre-configured HTTP client for user-service — baseURL is automatically prepended to every request
// so userAPI.post('/login/') becomes http://127.0.0.1:8003/api/users/login/
export const userAPI = axios.create({ baseURL: "http://127.0.0.1:8003/api/users" });



