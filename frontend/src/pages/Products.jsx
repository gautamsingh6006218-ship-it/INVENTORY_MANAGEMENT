import React, { useState, useEffect } from 'react';
// productAPI has JWT token automatically attached via interceptor in axios.js
import { productAPI } from '../api/axios';
import './Products.css';

function Products() {
    // product lists — one per category
    const [electronics, setElectronics] = useState([]);
    const [food, setFood] = useState([]);
    const [clothing, setClothing] = useState([]);

    // categories fetched from backend — used to populate the category dropdown in the form
    const [categories, setCategories] = useState([]);

    // controls whether the add product form is visible
    const [showForm, setShowForm] = useState(false);

    // which product type the user is adding — determines which extra fields to show
    const [productType, setProductType] = useState('electronics');

    // common fields shared by all product types
    const [name, setName] = useState('');
    const [sku, setSku] = useState('');
    const [price, setPrice] = useState('');
    const [category, setCategory] = useState('');

    // electronics-specific fields
    const [brand, setBrand] = useState('');
    const [warrantyYears, setWarrantyYears] = useState(1);

    // food-specific fields
    const [expiryDate, setExpiryDate] = useState('');
    const [isOrganic, setIsOrganic] = useState(false);

    // clothing-specific fields
    const [size, setSize] = useState('');
    const [material, setMaterial] = useState('');

    const [error, setError] = useState('');

    // runs once on page load — fetches all products and categories
    useEffect(() => {
        fetchAllProducts();
        // categories are needed for the form dropdown
        productAPI.get('/categories/')
            .then(response => setCategories(response.data))
            .catch(err => console.log(err));
    }, []);

    // separate function so we can call it again after adding a product to refresh the table
    const fetchAllProducts = () => {
        productAPI.get('/electronics/')
            .then(response => setElectronics(response.data))
            .catch(err => console.log(err));

        productAPI.get('/food/')
            .then(response => setFood(response.data))
            .catch(err => console.log(err));

        productAPI.get('/clothing/')
            .then(response => setClothing(response.data))
            .catch(err => console.log(err));
    };

    const handleAddProduct = async () => {
        setError('');
        // build the payload — common fields first, then type-specific ones
        const common = { name, sku, price, category };

        try {
            if (productType === 'electronics') {
                // warrenty_years matches the typo in the backend model field name
                await productAPI.post('/electronics/', { ...common, brand, warrenty_years: warrantyYears });
            } else if (productType === 'food') {
                await productAPI.post('/food/', { ...common, expiry_date: expiryDate, is_organic: isOrganic });
            } else {
                await productAPI.post('/clothing/', { ...common, size, material });
            }
            // refresh tables so new product appears immediately
            fetchAllProducts();
            // reset form fields
            setName(''); setSku(''); setPrice(''); setCategory('');
            setBrand(''); setWarrantyYears(1);
            setExpiryDate(''); setIsOrganic(false);
            setSize(''); setMaterial('');
            setShowForm(false);
        } catch (err) {
            const data = err.response?.data;
            if (data) {
                const firstError = Object.values(data)[0];
                setError(Array.isArray(firstError) ? firstError[0] : firstError);
            } else {
                setError('Failed to add product.');
            }
        }
    };

    return (
        <div className="page">
            <div className="page-header">
                <h2>Products</h2>
                {/* toggle button — shows/hides the add product form */}
                <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
                    {showForm ? 'Cancel' : '+ Add Product'}
                </button>
            </div>

            {/* add product form — only shown when showForm is true */}
            {showForm && (
                <div className="form-card">
                    <h3>Add New Product</h3>
                    {error && <p className="form-error">{error}</p>}

                    {/* product type selector — controls which extra fields appear below */}
                    <div className="form-row">
                        <label>Product Type</label>
                        <select value={productType} onChange={(e) => setProductType(e.target.value)}>
                            <option value="electronics">Electronics</option>
                            <option value="food">Food</option>
                            <option value="clothing">Clothing</option>
                        </select>
                    </div>

                    {/* common fields — same for all product types */}
                    <div className="form-row">
                        <label>Name</label>
                        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Product name" />
                    </div>
                    <div className="form-row">
                        <label>SKU</label>
                        <input value={sku} onChange={(e) => setSku(e.target.value)} placeholder="Unique SKU code" />
                    </div>
                    <div className="form-row">
                        <label>Price</label>
                        <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} placeholder="0.00" />
                    </div>
                    <div className="form-row">
                        <label>Category</label>
                        {/* populated from /categories/ endpoint — sends category ID to backend */}
                        <select value={category} onChange={(e) => setCategory(e.target.value)}>
                            <option value="">Select category</option>
                            {categories.map(cat => (
                                <option key={cat.id} value={cat.id}>{cat.name}</option>
                            ))}
                        </select>
                    </div>

                    {/* electronics-specific fields — only shown when productType is electronics */}
                    {productType === 'electronics' && (
                        <>
                            <div className="form-row">
                                <label>Brand</label>
                                <input value={brand} onChange={(e) => setBrand(e.target.value)} placeholder="Brand name" />
                            </div>
                            <div className="form-row">
                                <label>Warranty (years)</label>
                                <input type="number" value={warrantyYears} onChange={(e) => setWarrantyYears(e.target.value)} />
                            </div>
                        </>
                    )}

                    {/* food-specific fields — only shown when productType is food */}
                    {productType === 'food' && (
                        <>
                            <div className="form-row">
                                <label>Expiry Date</label>
                                <input type="date" value={expiryDate} onChange={(e) => setExpiryDate(e.target.value)} />
                            </div>
                            <div className="form-row checkbox-row">
                                <label>Organic</label>
                                {/* checkbox — checked state maps to is_organic boolean on backend */}
                                <input type="checkbox" checked={isOrganic} onChange={(e) => setIsOrganic(e.target.checked)} />
                            </div>
                        </>
                    )}

                    {/* clothing-specific fields — only shown when productType is clothing */}
                    {productType === 'clothing' && (
                        <>
                            <div className="form-row">
                                <label>Size</label>
                                <input value={size} onChange={(e) => setSize(e.target.value)} placeholder="e.g. M, L, XL" />
                            </div>
                            <div className="form-row">
                                <label>Material</label>
                                <input value={material} onChange={(e) => setMaterial(e.target.value)} placeholder="e.g. Cotton" />
                            </div>
                        </>
                    )}

                    <button className="btn-submit" onClick={handleAddProduct}>Add Product</button>
                </div>
            )}

            {/* electronics table */}
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

            {/* food table */}
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
                            <td>{product.is_organic ? 'Yes' : 'No'}</td>
                            <td>${product.price}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* clothing table */}
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
