import React, { useState, useEffect } from "react";
// pulling from all services to build a summary view
import { productAPI, inventoryAPI, orderAPI, notificationAPI } from "../api/axios";
import "./Dashboard.css";

function Dashboard() {
    // stat card counts — each fetched from a different microservice
    const [totalProducts, setTotalProducts] = useState(0);
    const [totalOrders, setTotalOrders] = useState(0);
    const [lowStockCount, setLowStockCount] = useState(0);
    const [unreadCount, setUnreadCount] = useState(0);

    // recent data for the tables below the stat cards
    const [recentOrders, setRecentOrders] = useState([]);
    const [recentNotifications, setRecentNotifications] = useState([]);

    // runs once on page load — fetches data from all 4 services in parallel
    useEffect(() => {
        // sum electronics + food + clothing to get total product count
        Promise.all([
            productAPI.get('/electronics/'),
            productAPI.get('/food/'),
            productAPI.get('/clothing/')
        ]).then(([e, f, c]) => {
            setTotalProducts(e.data.length + f.data.length + c.data.length);
        }).catch(err => console.log(err));

        // inventory — count items where quantity is at or below reorder_level
        inventoryAPI.get('/').then(response => {
            const low = response.data.filter(item => item.quantity <= item.reorder_level);
            setLowStockCount(low.length);
        }).catch(err => console.log(err));

        // orders — total count + last 5 for the recent orders table
        orderAPI.get('/').then(response => {
            setTotalOrders(response.data.length);
            // slice(-5) takes last 5 items, reverse() shows newest first
            setRecentOrders(response.data.slice(-5).reverse());
        }).catch(err => console.log(err));

        // notifications — unread count + last 5 for the recent list
        notificationAPI.get('/').then(response => {
            const unread = response.data.filter(n => !n.is_read);
            setUnreadCount(unread.length);
            setRecentNotifications(response.data.slice(-5).reverse());
        }).catch(err => console.log(err));
    }, []);

    return (
        <div className="page">
            <h2>Dashboard</h2>

            {/* stat cards — one per service, shows a key number at a glance */}
            <div className="stat-grid">
                <div className="stat-card">
                    <span className="stat-label">Total Products</span>
                    <span className="stat-value">{totalProducts}</span>
                </div>
                <div className="stat-card">
                    <span className="stat-label">Total Orders</span>
                    <span className="stat-value">{totalOrders}</span>
                </div>
                {/* low stock card turns red when there are items needing restock */}
                <div className={`stat-card ${lowStockCount > 0 ? 'stat-card--warning' : ''}`}>
                    <span className="stat-label">Low Stock Items</span>
                    <span className="stat-value">{lowStockCount}</span>
                </div>
                <div className={`stat-card ${unreadCount > 0 ? 'stat-card--alert' : ''}`}>
                    <span className="stat-label">Unread Notifications</span>
                    <span className="stat-value">{unreadCount}</span>
                </div>
            </div>

            {/* bottom section — two panels side by side */}
            <div className="dashboard-panels">

                {/* recent orders panel */}
                <div className="panel">
                    <h3>Recent Orders</h3>
                    <table className="dashboard-table">
                        <thead>
                            <tr>
                                <th>Order ID</th>
                                <th>Product</th>
                                <th>Qty</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {recentOrders.map(order => (
                                <tr key={order.id}>
                                    <td>#{order.id}</td>
                                    <td>{order.product_id}</td>
                                    <td>{order.quantity}</td>
                                    <td>
                                        <span className={`status-badge status-${order.status.toLowerCase()}`}>
                                            {order.status}
                                        </span>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {/* recent notifications panel */}
                <div className="panel">
                    <h3>Recent Notifications</h3>
                    {recentNotifications.map(n => (
                        // unread notifications get the highlighted border
                        <div key={n.id} className={`notif-item ${!n.is_read ? 'notif-item--unread' : ''}`}>
                            <p>{n.message}</p>
                            <span className="notif-status">{n.is_read ? 'Read' : 'Unread'}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
