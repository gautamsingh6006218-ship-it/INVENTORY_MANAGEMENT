import React, { useState } from "react";
import { userAPI } from "../api/axios";
import { useNavigate, Link } from "react-router-dom";
import "./Login.css";

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errors, setErrors] = useState({});
    const navigate = useNavigate();

    // validate returns false if any field fails — sets errors so they show under each input
    const validate = () => {
        const errs = {};
        if (!email.trim()) errs.email = "Email is required";
        else if (!/\S+@\S+\.\S+/.test(email)) errs.email = "Invalid email format";
        if (!password) errs.password = "Password is required";
        setErrors(errs);
        return Object.keys(errs).length === 0;
    };

    const handleLogin = async () => {
        if (!validate()) return;
        try {
            const response = await userAPI.post("/login/", { email, password });
            localStorage.setItem("token", response.data.access);
            localStorage.setItem("refresh", response.data.refresh);
            navigate("/dashboard");
        } catch (error) {
            setErrors({ api: "Invalid email or password" });
        }
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            {errors.api && <p className="field-error" style={{ textAlign: 'center' }}>{errors.api}</p>}
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            {errors.email && <p className="field-error">{errors.email}</p>}
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            {errors.password && <p className="field-error">{errors.password}</p>}
            <button onClick={handleLogin}>Login</button>
            <p className="login-link">
                Don't have an account? <Link to="/register">Register</Link>
            </p>
        </div>
    );
}

export default Login;
