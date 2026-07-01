import React, { useState } from "react";
import { userAPI } from "../api/axios";
import { useNavigate, Link } from "react-router-dom";
import "./Register.css";

function Register() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("staff");
    const [phone, setPhone] = useState("");
    const [errors, setErrors] = useState({});

    const navigate = useNavigate();

    const validate = () => {
        const errs = {};
        if (!username.trim()) errs.username = "Username is required";
        if (!email.trim()) errs.email = "Email is required";
        else if (!/\S+@\S+\.\S+/.test(email)) errs.email = "Invalid email format";
        if (!password) errs.password = "Password is required";
        else if (password.length < 6) errs.password = "Password must be at least 6 characters";
        setErrors(errs);
        return Object.keys(errs).length === 0;
    };

    const handleRegister = async () => {
        if (!validate()) return;
        try {
            await userAPI.post("/register/", { username, email, password, role, phone });
            navigate("/");
        } catch (err) {
            const data = err.response?.data;
            if (data) {
                const firstError = Object.values(data)[0];
                setErrors({ api: Array.isArray(firstError) ? firstError[0] : firstError });
            } else {
                setErrors({ api: "Registration failed. Please try again." });
            }
        }
    };

    return (
        <div className="register-container">
            <h2>Create Account</h2>
            {errors.api && <p className="register-error">{errors.api}</p>}

            <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
            {errors.username && <p className="field-error">{errors.username}</p>}

            <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
            {errors.email && <p className="field-error">{errors.email}</p>}

            <input type="password" placeholder="Password (min 6 characters)" value={password} onChange={(e) => setPassword(e.target.value)} />
            {errors.password && <p className="field-error">{errors.password}</p>}

            <input type="text" placeholder="Phone (optional)" value={phone} onChange={(e) => setPhone(e.target.value)} />

            <select value={role} onChange={(e) => setRole(e.target.value)}>
                <option value="staff">Staff</option>
                <option value="admin">Admin</option>
                <option value="manager">Manager</option>
            </select>

            <button onClick={handleRegister}>Register</button>
            <p className="register-link">
                Already have an account? <Link to="/">Login</Link>
            </p>
        </div>
    );
}

export default Register;
