import React, { useState } from "react";
// userAPI has baseURL pre-set to user-service — no need to write full URL every time
import { userAPI } from "../api/axios";

function Login() {

    // state to store what user types — React re-renders whenever these change
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    // async because API call to backend takes time — await waits for response before proceeding
    const handleLogin = async () => {
        try {
            // sends email and password as JSON to POST /login/ on user-service
            const response = await userAPI.post("/login/", { email, password });
            // saves JWT token in localStorage so other pages can attach it to requests
            localStorage.setItem("token", response.data.access);
            alert("Login successful");
        } catch (error) {
            // backend returns 401 if credentials are wrong — caught here
            alert("Invalid email or password");
        }
    };

    return (
        <div>
            <h2>Login</h2>
            {/* value and onChange make this a controlled input — React tracks every keystroke */}
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            {/* onClick triggers handleLogin which calls the backend */}
            <button onClick={handleLogin}>Login</button>
        </div>
    );
}

export default Login;