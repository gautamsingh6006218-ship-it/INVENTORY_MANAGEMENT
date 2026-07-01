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
            {/* map loops through each order and renders customer_id and status */}
            {orders.map(order => (
                <div className="card" key={order.id}>
                    <p>Order #{order.id} — Product: {order.product_id} — Qty: {order.quantity} — Status: {order.status}</p>
                </div>
            ))}
        </div>
    );
}

export default Orders;