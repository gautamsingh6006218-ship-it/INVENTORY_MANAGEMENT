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

            {/* Electronics table — columns specific to electronics products */}
            <h3>Electronics</h3>
            <table className="product-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>SKU</th>
                        <th>Brand</th>
                        <th>Warranty (yrs)</th>
                        <th>Price</th>
                    </tr>
                </thead>
                <tbody>
                    {electronics.map(product => (
                        <tr key={product.id}>
                            <td>{product.name}</td>
                            <td>{product.sku}</td>
                            <td>{product.brand}</td>
                            <td>{product.warrenty_years}</td>
                            <td>${product.price}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* Food table — columns specific to food products */}
            <h3>Food</h3>
            <table className="product-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>SKU</th>
                        <th>Expiry Date</th>
                        <th>Organic</th>
                        <th>Price</th>
                    </tr>
                </thead>
                <tbody>
                    {food.map(product => (
                        <tr key={product.id}>
                            <td>{product.name}</td>
                            <td>{product.sku}</td>
                            <td>{product.expiry_date}</td>
                            {/* shows Yes/No instead of true/false for readability */}
                            <td>{product.is_organic ? 'Yes' : 'No'}</td>
                            <td>${product.price}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* Clothing table — columns specific to clothing products */}
            <h3>Clothing</h3>
            <table className="product-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>SKU</th>
                        <th>Size</th>
                        <th>Material</th>
                        <th>Price</th>
                    </tr>
                </thead>
                <tbody>
                    {clothing.map(product => (
                        <tr key={product.id}>
                            <td>{product.name}</td>
                            <td>{product.sku}</td>
                            <td>{product.size}</td>
                            <td>{product.material}</td>
                            <td>${product.price}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Products;
