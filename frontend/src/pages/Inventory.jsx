import React, { useState, useEffect } from 'react';
// inventoryAPI has JWT token automatically attached via interceptor in axios.js
import { inventoryAPI } from '../api/axios';
import './Inventory.css';

function Inventory() {
    // holds array of stock entries fetched from inventory-service
    const [stock, setStock] = useState([]);

    // runs once on page load — fetches all stock entries from inventory-service
    useEffect(() => {
        inventoryAPI.get('/')
            .then(response => setStock(response.data))
            .catch(error => console.log(error));
    }, []);

    return (
        <div className="page">
            <h2>Inventory</h2>
            <table className="inventory-table">
                <thead>
                    <tr>
                        <th>Product ID</th>
                        <th>Quantity</th>
                        <th>Warehouse Location</th>
                        <th>Reorder Level</th>
                        <th>Last Updated</th>
                    </tr>
                </thead>
                <tbody>
                    {/* map loops through each stock entry and renders all fields as a row */}
                    {stock.map(item => (
                        <tr key={item.id}>
                            <td>{item.product_id}</td>
                            <td>
                                {/* highlight low stock in red — quantity at or below reorder_level means restock needed */}
                                <span className={item.quantity <= item.reorder_level ? 'low-stock' : ''}>
                                    {item.quantity}
                                </span>
                            </td>
                            <td>{item.warehouse_location}</td>
                            <td>{item.reorder_level}</td>
                            {/* slice(0, 10) extracts just the date part from ISO datetime string */}
                            <td>{item.last_updated.slice(0, 10)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Inventory;
