import React from "react";
import { Navigate } from "react-router-dom";

function ProtectedRoute({ children }) {
    const token = localStorage.getItem("token");

    if (!token) {
        // no token in localStorage — user is not logged in, send them to login
        return <Navigate to="/" replace />;
    }

    // decode the JWT payload to check if it has expired
    // JWT format is header.payload.signature — payload is base64 encoded JSON
    try {
        const payload = JSON.parse(atob(token.split(".")[1]));
        const isExpired = payload.exp * 1000 < Date.now(); // exp is in seconds, Date.now() is ms

        if (isExpired) {
            // clear stale tokens so they don't linger in localStorage
            localStorage.removeItem("token");
            localStorage.removeItem("refresh");
            return <Navigate to="/" replace />;
        }
    } catch {
        // token is malformed — treat as not logged in
        localStorage.removeItem("token");
        localStorage.removeItem("refresh");
        return <Navigate to="/" replace />;
    }

    // token exists and is valid — render the requested page
    return children;
}

export default ProtectedRoute;
