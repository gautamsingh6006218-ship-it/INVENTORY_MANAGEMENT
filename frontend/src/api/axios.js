import axios from "axios";

// pre-configured HTTP client for user-service — baseURL is automatically prepended to every request
// so userAPI.post('/login/') becomes http://127.0.0.1:8003/api/users/login/
export const userAPI = axios.create({ baseURL: "http://127.0.0.1:8003/api/users" });
export const productAPI = axios.create({ baseURL: 'http://127.0.0.1:8000/api/products' });
export const inventoryAPI = axios.create({ baseURL: 'http://127.0.0.1:8001/api/inventory' });
export const orderAPI = axios.create({ baseURL: 'http://127.0.0.1:8002/api/orders' });
export const notificationAPI = axios.create({ baseURL: 'http://127.0.0.1:8007/api/notifications' });
export const supplierAPI = axios.create({ baseURL: 'http://127.0.0.1:8004/api' });
export const discountAPI = axios.create({ baseURL: 'http://127.0.0.1:8005/api' });
export const reportAPI = axios.create({ baseURL: 'http://127.0.0.1:8006/api' });

const attachToken = (instance) => {
    // request interceptor — attaches JWT token to every outgoing request
    instance.interceptors.request.use((config) => {
        const token = localStorage.getItem("token");
        if (token) config.headers.Authorization = `Bearer ${token}`;
        return config;
    });

    // response interceptor — if any API returns 401 (token expired/invalid), redirect to login
    instance.interceptors.response.use(
        (response) => response,
        (error) => {
            if (error.response?.status === 401) {
                localStorage.removeItem("token");
                localStorage.removeItem("refresh");
                // window.location.href works outside React components unlike useNavigate
                window.location.href = "/";
            }
            return Promise.reject(error);
        }
    );
};
attachToken(userAPI);
attachToken(productAPI);
attachToken(inventoryAPI);
attachToken(orderAPI);
attachToken(notificationAPI);
attachToken(supplierAPI);
attachToken(discountAPI);
attachToken(reportAPI);

