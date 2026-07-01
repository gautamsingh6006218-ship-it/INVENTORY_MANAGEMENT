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

const attachToken = (instance) => {
    instance.interceptors.request.use((config) => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    });
};
attachToken(productAPI);
attachToken(inventoryAPI);
attachToken(orderAPI);
attachToken(notificationAPI);
attachToken(supplierAPI);
attachToken(discountAPI);

