import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Products from './pages/Products';
import Inventory from './pages/Inventory';
import Orders from './pages/Orders';
import Notifications from './pages/Notifications';
import Suppliers from './pages/Suppliers';
import Discounts from './pages/Discounts';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import './App.css';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                {/* public routes — no token required */}
                <Route path="/" element={<Login />} />
                <Route path="/register" element={<Register />} />

                {/* protected routes — ProtectedRoute checks token before rendering the page */}
                <Route path="/dashboard" element={<ProtectedRoute><Navbar /><Dashboard /></ProtectedRoute>} />
                <Route path="/products" element={<ProtectedRoute><Navbar /><Products /></ProtectedRoute>} />
                <Route path="/inventory" element={<ProtectedRoute><Navbar /><Inventory /></ProtectedRoute>} />
                <Route path="/orders" element={<ProtectedRoute><Navbar /><Orders /></ProtectedRoute>} />
                <Route path="/notifications" element={<ProtectedRoute><Navbar /><Notifications /></ProtectedRoute>} />
                <Route path="/suppliers" element={<ProtectedRoute><Navbar /><Suppliers /></ProtectedRoute>} />
                <Route path="/discounts" element={<ProtectedRoute><Navbar /><Discounts /></ProtectedRoute>} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
