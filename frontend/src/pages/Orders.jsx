import React, { useState, useEffect } from 'react';
import { orderAPI } from '../api/axios';
import ConfirmModal from '../components/ConfirmModal';
import './Orders.css';

function Orders() {
    const [orders, setOrders] = useState([]);
    const [showForm, setShowForm] = useState(false);
    const [customerId, setCustomerId] = useState('');
    const [productId, setProductId] = useState('');
    const [quantity, setQuantity] = useState('');
    const [totalPrice, setTotalPrice] = useState('');
    const [error, setError] = useState('');
    const [errors, setErrors] = useState({});
    const [pendingDeleteId, setPendingDeleteId] = useState(null);

    useEffect(() => {
        fetchOrders();
    }, []);

    const fetchOrders = () => {
        orderAPI.get('/')
            .then(response => setOrders(response.data))
            .catch(err => console.log(err));
    };

    const validate = () => {
        const errs = {};
        if (!customerId) errs.customerId = 'Customer ID is required';
        if (!productId) errs.productId = 'Product ID is required';
        if (!quantity || quantity <= 0) errs.quantity = 'Quantity must be greater than 0';
        if (!totalPrice || totalPrice <= 0) errs.totalPrice = 'Total price must be greater than 0';
        setErrors(errs);
        return Object.keys(errs).length === 0;
    };

    const handlePlaceOrder = async () => {
        if (!validate()) return;
        setError('');
        try {
            await orderAPI.post('/', {
                customer_id: customerId,
                product_id: productId,
                quantity,
                total_price: totalPrice,
            });
            fetchOrders();
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

    // PATCH /orders/:id/status/ — only updates the status field, rest of order unchanged
    const handleUpdateStatus = async (id, newStatus) => {
        try {
            await orderAPI.patch(`/${id}/status/`, { status: newStatus });
            // update the local state directly so table reflects change without a full refetch
            setOrders(orders.map(o => o.id === id ? { ...o, status: newStatus } : o));
        } catch (err) {
            console.log(err);
        }
    };

    // DELETE /orders/:id/ — removes order permanently from DB
    const handleDelete = async (id) => {
        try {
            await orderAPI.delete(`/${id}/`);
            // remove deleted order from local state so table updates immediately
            setOrders(orders.filter(o => o.id !== id));
        } catch (err) {
            console.log(err);
        }
    };

    return (
        <div className="page">
            <div className="page-header">
                <h2>Orders</h2>
                <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
                    {showForm ? 'Cancel' : '+ Place Order'}
                </button>
            </div>

            {showForm && (
                <div className="form-card">
                    <h3>Place New Order</h3>
                    {error && <p className="form-error">{error}</p>}
                    <div className="form-row">
                        <label>Customer ID</label>
                        <input type="number" value={customerId} onChange={(e) => setCustomerId(e.target.value)} placeholder="Customer ID" />
                    </div>
                    {errors.customerId && <p className="field-error">{errors.customerId}</p>}
                    <div className="form-row">
                        <label>Product ID</label>
                        <input type="number" value={productId} onChange={(e) => setProductId(e.target.value)} placeholder="Product ID" />
                    </div>
                    {errors.productId && <p className="field-error">{errors.productId}</p>}
                    <div className="form-row">
                        <label>Quantity</label>
                        <input type="number" value={quantity} onChange={(e) => setQuantity(e.target.value)} placeholder="Number of units" />
                    </div>
                    {errors.quantity && <p className="field-error">{errors.quantity}</p>}
                    <div className="form-row">
                        <label>Total Price</label>
                        <input type="number" value={totalPrice} onChange={(e) => setTotalPrice(e.target.value)} placeholder="0.00" />
                    </div>
                    {errors.totalPrice && <p className="field-error">{errors.totalPrice}</p>}
                    <button className="btn-submit" onClick={handlePlaceOrder}>Place Order</button>
                </div>
            )}

            <table className="orders-table">
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Customer ID</th>
                        <th>Product ID</th>
                        <th>Quantity</th>
                        <th>Total Price</th>
                        {/* status column uses an inline dropdown — change fires PATCH immediately */}
                        <th>Status</th>
                        <th>Created At</th>
                        <th>Actions</th>
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
                            <td>
                                {/* dropdown instead of a badge — selecting a new value calls PATCH */}
                                <select
                                    className={`status-select status-${order.status.toLowerCase()}`}
                                    value={order.status}
                                    onChange={(e) => handleUpdateStatus(order.id, e.target.value)}
                                >
                                    <option value="Pending">Pending</option>
                                    <option value="Processing">Processing</option>
                                    <option value="Delivered">Delivered</option>
                                    <option value="Cancelled">Cancelled</option>
                                </select>
                            </td>
                            <td>{order.created_at.slice(0, 10)}</td>
                            <td>
                                <button className="btn-delete" onClick={() => setPendingDeleteId(order.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        {pendingDeleteId && (
            <ConfirmModal
                message="Delete this order? This cannot be undone."
                onConfirm={() => { handleDelete(pendingDeleteId); setPendingDeleteId(null); }}
                onCancel={() => setPendingDeleteId(null)}
            />
        )}
        </div>
    );
}

export default Orders;
