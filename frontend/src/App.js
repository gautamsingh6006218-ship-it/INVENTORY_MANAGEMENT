import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Products from './pages/Products';
import Inventory from './pages/Inventory';
import Orders from './pages/Orders';
import Notifications from './pages/Notifications';
import Navbar from './components/Navbar';
import './App.css';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/dashboard" element={<><Navbar /><Dashboard /></>} />
                <Route path="/products" element={<><Navbar /><Products /></>} />
                <Route path="/inventory" element={<><Navbar /><Inventory /></>} />
                <Route path="/orders" element={<><Navbar /><Orders /></>} />
                <Route path="/notifications" element={<><Navbar /><Notifications /></>} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
