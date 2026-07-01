import React, { useState } from "react";
import { userAPI } from "../api/axios";
import { useNavigate, Link } from "react-router-dom";
import "./Register.css";

function Register() {
    // one state per form field — React tracks every keystroke via onChange
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("staff");
    const [phone, setPhone] = useState("");
    const [error, setError] = useState("");

    const navigate = useNavigate();

    // async because POST to backend takes time — await pauses until response comes back
    const handleRegister = async () => {
        setError("");
        try {
            // sends all fields to POST /register/ — role and phone are optional on backend
            await userAPI.post("/register/", { username, email, password, role, phone });
            // on success, redirect to login so user can sign in with their new account
            navigate("/");
        } catch (err) {
            // backend returns field-level errors e.g. { email: ["already exists"] }
            const data = err.response?.data;
            if (data) {
                // grab first error message from whatever field failed
                const firstError = Object.values(data)[0];
                setError(Array.isArray(firstError) ? firstError[0] : firstError);
            } else {
                setError("Registration failed. Please try again.");
            }
        }
    };

    return (
        <div className="register-container">
            <h2>Create Account</h2>

            {/* show backend error message if registration fails */}
            {error && <p className="register-error">{error}</p>}

            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password (min 6 characters)"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <input
                type="text"
                placeholder="Phone (optional)"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
            />

            {/* dropdown for role — backend defaults to 'staff' if not sent */}
            <select value={role} onChange={(e) => setRole(e.target.value)}>
                <option value="staff">Staff</option>
                <option value="admin">Admin</option>
                <option value="manager">Manager</option>
            </select>

            <button onClick={handleRegister}>Register</button>

            {/* link back to login for users who already have an account */}
            <p className="register-link">
                Already have an account? <Link to="/">Login</Link>
            </p>
        </div>
    );
}

export default Register;
