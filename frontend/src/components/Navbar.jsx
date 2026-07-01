import React from "react";
import { userAPI } from "../api/axios";
import { useNavigate, NavLink } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            const refresh = localStorage.getItem("refresh");
            await userAPI.post("/logout/", { refresh });
        } catch (error) {}
        localStorage.removeItem("token");
        localStorage.removeItem("refresh");
        navigate("/");
    };

    // NavLink's className prop receives { isActive } — returns different class based on current URL
    const linkClass = ({ isActive }) => isActive ? "nav-link nav-link--active" : "nav-link";

    return (
        <nav>
            {/* logo — always on the far left */}
            <span className="nav-brand">Inventory Management</span>

            {/* main navigation links — center section */}
            <div className="nav-links">
                <NavLink to="/dashboard" className={linkClass}>Dashboard</NavLink>
                <NavLink to="/products" className={linkClass}>Products</NavLink>
                <NavLink to="/inventory" className={linkClass}>Inventory</NavLink>
                <NavLink to="/orders" className={linkClass}>Orders</NavLink>
                <NavLink to="/notifications" className={linkClass}>Notifications</NavLink>
                <NavLink to="/suppliers" className={linkClass}>Suppliers</NavLink>
                <NavLink to="/discounts" className={linkClass}>Discounts</NavLink>
            </div>

            {/* user section — always on the far right */}
            <div className="nav-user">
                <NavLink to="/profile" className={linkClass}>Profile</NavLink>
                <button className="nav-logout" onClick={handleLogout}>Logout</button>
            </div>
        </nav>
    );
}

export default Navbar;
