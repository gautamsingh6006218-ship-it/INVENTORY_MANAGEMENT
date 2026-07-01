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
            {/* map loops through each stock entry and renders product_id and quantity */}
            {stock.map(product => (
                <div className="card" key={product.id}>
                    <p>{product.product_id} — {product.quantity} units</p>
                </div>
            ))}
        </div>
    );
}

export default Inventory;