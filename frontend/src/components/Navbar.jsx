import React from "react";
import { userAPI } from "../api/axios";
import { useNavigate, Link } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
    const navigate = useNavigate();

    const handleLogout = async () => {
        try{
            const refresh = localStorage.getItem("refresh");
            await userAPI.post("/logout/", { refresh });
        } catch (error) {
            
        }
        // removes JWT token from localStorage
        localStorage.removeItem("token");
        localStorage.removeItem("refresh");
        navigate("/");
    };

    return (
        <nav>
            <h2>Inventory Management</h2>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/products">Products</Link>
            <Link to="/inventory">Inventory</Link>
            <Link to="/orders">Orders</Link>
            <Link to="/notifications">Notifications</Link>
            <Link to="/suppliers">Suppliers</Link>
            <Link to="/discounts">Discounts</Link>

            <button onClick={handleLogout}>Logout</button>
        </nav>
    );
}

export default Navbar;