import React, { useState, useEffect } from "react";
import { productAPI, inventoryAPI, orderAPI, notificationAPI } from "../api/axios";
import "./Dashboard.css";

function Dashboard() {
    const [totalProducts, setTotalProducts] = useState(0);
    const [totalOrders, setTotalOrders] = useState(0);
    const [lowStockItems, setLowStockItems] = useState([]);
    const [unreadCount, setUnreadCount] = useState(0);
    const [recentOrders, setRecentOrders] = useState([]);
    const [recentNotifications, setRecentNotifications] = useState([]);

    useEffect(() => {
        Promise.all([
            productAPI.get('/electronics/'),
            productAPI.get('/food/'),
            productAPI.get('/clothing/')
        ]).then(([e, f, c]) => {
            setTotalProducts(e.data.length + f.data.length + c.data.length);
        }).catch(console.log);

        inventoryAPI.get('/').then(response => {
            // keep the full low-stock items so we can list them in the panel
            const low = response.data.filter(item => item.quantity <= item.reorder_level);
            setLowStockItems(low);
        }).catch(console.log);

        orderAPI.get('/').then(response => {
            setTotalOrders(response.data.length);
            setRecentOrders(response.data.slice(-5).reverse());
        }).catch(console.log);

        notificationAPI.get('/').then(response => {
            const unread = response.data.filter(n => !n.is_read);
            setUnreadCount(unread.length);
            setRecentNotifications(response.data.slice(-5).reverse());
        }).catch(console.log);
    }, []);

    return (
        <div className="page">
            <h2>Dashboard</h2>

            {/* stat cards */}
            <div className="stat-grid">
                <div className="stat-card">
                    <span className="stat-label">Total Products</span>
                    <span className="stat-value">{totalProducts}</span>
                </div>
                <div className="stat-card">
                    <span className="stat-label">Total Orders</span>
                    <span className="stat-value">{totalOrders}</span>
                </div>
                <div className={`stat-card ${lowStockItems.length > 0 ? 'stat-card--warning' : ''}`}>
                    <span className="stat-label">Low Stock Items</span>
                    <span className="stat-value">{lowStockItems.length}</span>
                </div>
                <div className={`stat-card ${unreadCount > 0 ? 'stat-card--alert' : ''}`}>
                    <span className="stat-label">Unread Notifications</span>
                    <span className="stat-value">{unreadCount}</span>
                </div>
            </div>

            <div className="dashboard-panels">

                {/* left panel — recent orders */}
                <div className="panel">
                    <h3>Recent Orders</h3>
                    {recentOrders.length === 0 ? (
                        <p className="empty-state">No orders yet.</p>
                    ) : (
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
                    )}
                </div>

                {/* right panel — split into low stock + recent notifications */}
                <div className="panel">

                    {/* low stock section — shows products that need restocking */}
                    <h3>Low Stock Alerts</h3>
                    {lowStockItems.length === 0 ? (
                        <p className="empty-state">All stock levels are healthy.</p>
                    ) : (
                        lowStockItems.map(item => (
                            <div key={item.id} className="alert-item">
                                <span>Product #{item.product_id}</span>
                                <span className="alert-qty">{item.quantity} / {item.reorder_level} units</span>
                            </div>
                        ))
                    )}

                    <div className="panel-divider" />

                    {/* recent notifications section */}
                    <h3>Recent Notifications</h3>
                    {recentNotifications.length === 0 ? (
                        <p className="empty-state">No notifications yet.</p>
                    ) : (
                        recentNotifications.map(n => (
                            <div key={n.id} className={`notif-item ${!n.is_read ? 'notif-item--unread' : ''}`}>
                                <p>{n.message}</p>
                                <span className="notif-status">{n.is_read ? 'Read' : 'Unread'}</span>
                            </div>
                        ))
                    )}
                </div>

            </div>
        </div>
    );
}

export default Dashboard;
