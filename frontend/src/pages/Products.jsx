import React, { useState, useEffect } from 'react';
// productAPI has JWT token automatically attached via interceptor in axios.js
import { productAPI } from '../api/axios';
import './Products.css';

function Products() {
    // separate state for each category — each holds an array of products from backend
    const [electronics, setElectronics] = useState([]);
    const [food, setFood] = useState([]);
    const [clothing, setClothing] = useState([]);

    // [] means run once when page loads — fetches all three categories simultaneously
    useEffect(() => {
        // each category is a separate endpoint in product-service
        productAPI.get('/electronics/')
            .then(response => setElectronics(response.data))
            .catch(error => console.log(error));

        productAPI.get('/food/')
            .then(response => setFood(response.data))
            .catch(error => console.log(error));

        productAPI.get('/clothing/')
            .then(response => setClothing(response.data))
            .catch(error => console.log(error));
    }, []);

    return (
        <div className="page">
            <h2>Products</h2>
            <h3>Electronics</h3>
            {/* map loops through array and renders a card for each product */}
            {electronics.map(product => (
                <div className="card" key={product.id}>
                    <p>{product.name} — ${product.price}</p>
                </div>
            ))}
            <h3>Food</h3>
            {food.map(product => (
                <div className="card" key={product.id}>
                    <p>{product.name} — ${product.price}</p>
                </div>
            ))}
            <h3>Clothing</h3>
            {clothing.map(product => (
                <div className="card" key={product.id}>
                    <p>{product.name} — ${product.price}</p>
                </div>
            ))}
        </div>
    );
}

export default Products;
