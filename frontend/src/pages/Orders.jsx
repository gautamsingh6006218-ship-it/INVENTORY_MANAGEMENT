import React, { useState, useEffect } from 'react';
import { orderAPI } from '../api/axios';
import './Orders.css';

function Orders() {
    // holds array of orders fetched from order-service
    const [orders, setOrders] = useState([]);

    // runs once on page load — fetches all orders from order-service
    useEffect(() => {
        orderAPI.get('/')
            .then(response => setOrders(response.data))
            .catch(error => console.log(error));
    }, []);

    return (
        <div className="page">
            <h2>Orders</h2>
            <table className="orders-table">
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Customer ID</th>
                        <th>Product ID</th>
                        <th>Quantity</th>
                        <th>Total Price</th>
                        <th>Status</th>
                        <th>Created At</th>
                    </tr>
                </thead>
                <tbody>
                    {/* map loops through each order and renders all fields as a row */}
                    {orders.map(order => (
                        <tr key={order.id}>
                            <td>#{order.id}</td>
                            <td>{order.customer_id}</td>
                            <td>{order.product_id}</td>
                            <td>{order.quantity}</td>
                            <td>${order.total_price}</td>
                            {/* status badge — CSS class matches status value e.g. 'Pending', 'Delivered' */}
                            <td>
                                <span className={`status-badge status-${order.status.toLowerCase()}`}>
                                    {order.status}
                                </span>
                            </td>
                            {/* slice(0, 10) extracts just the date part from ISO datetime string */}
                            <td>{order.created_at.slice(0, 10)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Orders;
