import React, { useState, useEffect } from 'react';
import { orderAPI } from '../api/axios';
import './Orders.css';

function Orders() {
    // holds array of orders fetched from order-service
    const [orders, setOrders] = useState([]);

    // controls whether the place order form is visible
    const [showForm, setShowForm] = useState(false);

    // form fields — match the Order model fields
    const [customerId, setCustomerId] = useState('');
    const [productId, setProductId] = useState('');
    const [quantity, setQuantity] = useState('');
    const [totalPrice, setTotalPrice] = useState('');
    const [error, setError] = useState('');

    // runs once on page load — fetches all orders
    useEffect(() => {
        fetchOrders();
    }, []);

    // separate function so we can call it again after placing an order to refresh the table
    const fetchOrders = () => {
        orderAPI.get('/')
            .then(response => setOrders(response.data))
            .catch(err => console.log(err));
    };

    const handlePlaceOrder = async () => {
        setError('');
        try {
            // POST to order-service — Kafka event is fired on backend after save
            await orderAPI.post('/', {
                customer_id: customerId,
                product_id: productId,
                quantity,
                total_price: totalPrice,
            });
            // refresh the orders table so new order appears immediately
            fetchOrders();
            // reset form
            setCustomerId(''); setProductId(''); setQuantity(''); setTotalPrice('');
            setShowForm(false);
        } catch (err) {
            const data = err.response?.data;
            if (data) {
                const firstError = Object.values(data)[0];
                setError(Array.isArray(firstError) ? firstError[0] : firstError);
            } else {
                setError('Failed to place order.');
            }
        }
    };

    return (
        <div className="page">
            <div className="page-header">
                <h2>Orders</h2>
                {/* toggle button — shows/hides the place order form */}
                <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
                    {showForm ? 'Cancel' : '+ Place Order'}
                </button>
            </div>

            {/* place order form — only shown when showForm is true */}
            {showForm && (
                <div className="form-card">
                    <h3>Place New Order</h3>
                    {error && <p className="form-error">{error}</p>}

                    <div className="form-row">
                        <label>Customer ID</label>
                        <input type="number" value={customerId} onChange={(e) => setCustomerId(e.target.value)} placeholder="Customer ID" />
                    </div>
                    <div className="form-row">
                        <label>Product ID</label>
                        <input type="number" value={productId} onChange={(e) => setProductId(e.target.value)} placeholder="Product ID" />
                    </div>
                    <div className="form-row">
                        <label>Quantity</label>
                        <input type="number" value={quantity} onChange={(e) => setQuantity(e.target.value)} placeholder="Number of units" />
                    </div>
                    <div className="form-row">
                        <label>Total Price</label>
                        <input type="number" value={totalPrice} onChange={(e) => setTotalPrice(e.target.value)} placeholder="0.00" />
                    </div>

                    <button className="btn-submit" onClick={handlePlaceOrder}>Place Order</button>
                </div>
            )}

            {/* orders table */}
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
