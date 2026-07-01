import React, { useState, useEffect } from 'react';
import { productAPI } from '../api/axios';
import './Products.css';

function Products() {
    const [electronics, setElectronics] = useState([]);
    const [food, setFood] = useState([]);
    const [clothing, setClothing] = useState([]);
    const [categories, setCategories] = useState([]);

    // add form state
    const [showForm, setShowForm] = useState(false);
    const [productType, setProductType] = useState('electronics');
    const [name, setName] = useState('');
    const [sku, setSku] = useState('');
    const [price, setPrice] = useState('');
    const [category, setCategory] = useState('');
    const [brand, setBrand] = useState('');
    const [warrantyYears, setWarrantyYears] = useState(1);
    const [expiryDate, setExpiryDate] = useState('');
    const [isOrganic, setIsOrganic] = useState(false);
    const [size, setSize] = useState('');
    const [material, setMaterial] = useState('');
    const [addError, setAddError] = useState('');

    // edit form state — editingProduct holds the product object, editType its category
    // editData is a mutable copy of the product being edited
    const [editingProduct, setEditingProduct] = useState(null);
    const [editType, setEditType] = useState('');
    const [editData, setEditData] = useState({});
    const [editError, setEditError] = useState('');

    useEffect(() => {
        fetchAllProducts();
        productAPI.get('/categories/')
            .then(response => setCategories(response.data))
            .catch(err => console.log(err));
    }, []);

    const fetchAllProducts = () => {
        productAPI.get('/electronics/').then(r => setElectronics(r.data)).catch(console.log);
        productAPI.get('/food/').then(r => setFood(r.data)).catch(console.log);
        productAPI.get('/clothing/').then(r => setClothing(r.data)).catch(console.log);
    };

    const handleAddProduct = async () => {
        setAddError('');
        const common = { name, sku, price, category };
        try {
            if (productType === 'electronics') {
                await productAPI.post('/electronics/', { ...common, brand, warrenty_years: warrantyYears });
            } else if (productType === 'food') {
                await productAPI.post('/food/', { ...common, expiry_date: expiryDate, is_organic: isOrganic });
            } else {
                await productAPI.post('/clothing/', { ...common, size, material });
            }
            fetchAllProducts();
            setName(''); setSku(''); setPrice(''); setCategory('');
            setBrand(''); setWarrantyYears(1);
            setExpiryDate(''); setIsOrganic(false);
            setSize(''); setMaterial('');
            setShowForm(false);
        } catch (err) {
            const data = err.response?.data;
            if (data) {
                const firstError = Object.values(data)[0];
                setAddError(Array.isArray(firstError) ? firstError[0] : firstError);
            } else {
                setAddError('Failed to add product.');
            }
        }
    };

    // clicking Edit copies the product into editData so the form is pre-filled
    const handleEdit = (type, product) => {
        setEditType(type);
        setEditingProduct(product);
        setEditData({ ...product });
        setEditError('');
        setShowForm(false); // close add form if open
    };

    // PUT /electronics/:id/ (or food/clothing) — sends full updated product to backend
    const handleUpdate = async () => {
        setEditError('');
        try {
            await productAPI.put(`/${editType}/${editingProduct.id}/`, editData);
            fetchAllProducts();
            setEditingProduct(null);
            setEditData({});
        } catch (err) {
            const data = err.response?.data;
            if (data) {
                const firstError = Object.values(data)[0];
                setEditError(Array.isArray(firstError) ? firstError[0] : firstError);
            } else {
                setEditError('Failed to update product.');
            }
        }
    };

    // DELETE /electronics/:id/ (or food/clothing) — removes product permanently
    const handleDelete = async (type, id) => {
        try {
            await productAPI.delete(`/${type}/${id}/`);
            fetchAllProducts();
        } catch (err) {
            console.log(err);
        }
    };

    // helper — renders edit form pre-filled with editData fields for the given product type
    const renderEditForm = () => (
        <div className="form-card">
            <h3>Edit Product</h3>
            {editError && <p className="form-error">{editError}</p>}

            <div className="form-row">
                <label>Name</label>
                <input value={editData.name || ''} onChange={(e) => setEditData({ ...editData, name: e.target.value })} />
            </div>
            <div className="form-row">
                <label>SKU</label>
                <input value={editData.sku || ''} onChange={(e) => setEditData({ ...editData, sku: e.target.value })} />
            </div>
            <div className="form-row">
                <label>Price</label>
                <input type="number" value={editData.price || ''} onChange={(e) => setEditData({ ...editData, price: e.target.value })} />
            </div>
            <div className="form-row">
                <label>Category</label>
                <select value={editData.category || ''} onChange={(e) => setEditData({ ...editData, category: e.target.value })}>
                    <option value="">Select category</option>
                    {categories.map(cat => (
                        <option key={cat.id} value={cat.id}>{cat.name}</option>
                    ))}
                </select>
            </div>

            {/* type-specific fields — shown based on which table's Edit button was clicked */}
            {editType === 'electronics' && (
                <>
                    <div className="form-row">
                        <label>Brand</label>
                        <input value={editData.brand || ''} onChange={(e) => setEditData({ ...editData, brand: e.target.value })} />
                    </div>
                    <div className="form-row">
                        <label>Warranty (years)</label>
                        <input type="number" value={editData.warrenty_years || 1} onChange={(e) => setEditData({ ...editData, warrenty_years: e.target.value })} />
                    </div>
                </>
            )}
            {editType === 'food' && (
                <>
                    <div className="form-row">
                        <label>Expiry Date</label>
                        <input type="date" value={editData.expiry_date || ''} onChange={(e) => setEditData({ ...editData, expiry_date: e.target.value })} />
                    </div>
                    <div className="form-row checkbox-row">
                        <label>Organic</label>
                        <input type="checkbox" checked={editData.is_organic || false} onChange={(e) => setEditData({ ...editData, is_organic: e.target.checked })} />
                    </div>
                </>
            )}
            {editType === 'clothing' && (
                <>
                    <div className="form-row">
                        <label>Size</label>
                        <input value={editData.size || ''} onChange={(e) => setEditData({ ...editData, size: e.target.value })} />
                    </div>
                    <div className="form-row">
                        <label>Material</label>
                        <input value={editData.material || ''} onChange={(e) => setEditData({ ...editData, material: e.target.value })} />
                    </div>
                </>
            )}

            <div className="form-actions">
                <button className="btn-submit" onClick={handleUpdate}>Save Changes</button>
                {/* cancel clears editingProduct which hides this form */}
                <button className="btn-cancel" onClick={() => setEditingProduct(null)}>Cancel</button>
            </div>
        </div>
    );

    return (
        <div className="page">
            <div className="page-header">
                <h2>Products</h2>
                <button className="btn-primary" onClick={() => { setShowForm(!showForm); setEditingProduct(null); }}>
                    {showForm ? 'Cancel' : '+ Add Product'}
                </button>
            </div>

            {/* add product form */}
            {showForm && (
                <div className="form-card">
                    <h3>Add New Product</h3>
                    {addError && <p className="form-error">{addError}</p>}
                    <div className="form-row">
                        <label>Product Type</label>
                        <select value={productType} onChange={(e) => setProductType(e.target.value)}>
                            <option value="electronics">Electronics</option>
                            <option value="food">Food</option>
                            <option value="clothing">Clothing</option>
                        </select>
                    </div>
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
                        <select value={category} onChange={(e) => setCategory(e.target.value)}>
                            <option value="">Select category</option>
                            {categories.map(cat => (
                                <option key={cat.id} value={cat.id}>{cat.name}</option>
                            ))}
                        </select>
                    </div>
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
                    {productType === 'food' && (
                        <>
                            <div className="form-row">
                                <label>Expiry Date</label>
                                <input type="date" value={expiryDate} onChange={(e) => setExpiryDate(e.target.value)} />
                            </div>
                            <div className="form-row checkbox-row">
                                <label>Organic</label>
                                <input type="checkbox" checked={isOrganic} onChange={(e) => setIsOrganic(e.target.checked)} />
                            </div>
                        </>
                    )}
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

            {/* edit form — appears when a row's Edit button is clicked */}
            {editingProduct && renderEditForm()}

            {/* electronics table */}
            <h3>Electronics</h3>
            <table className="product-table">
                <thead>
                    <tr>
                        <th>Name</th><th>SKU</th><th>Brand</th><th>Warranty (yrs)</th><th>Price</th><th>Actions</th>
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
                            <td className="action-cell">
                                <button className="btn-edit" onClick={() => handleEdit('electronics', product)}>Edit</button>
                                <button className="btn-delete" onClick={() => handleDelete('electronics', product.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* food table */}
            <h3>Food</h3>
            <table className="product-table">
                <thead>
                    <tr>
                        <th>Name</th><th>SKU</th><th>Expiry Date</th><th>Organic</th><th>Price</th><th>Actions</th>
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
                            <td className="action-cell">
                                <button className="btn-edit" onClick={() => handleEdit('food', product)}>Edit</button>
                                <button className="btn-delete" onClick={() => handleDelete('food', product.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* clothing table */}
            <h3>Clothing</h3>
            <table className="product-table">
                <thead>
                    <tr>
                        <th>Name</th><th>SKU</th><th>Size</th><th>Material</th><th>Price</th><th>Actions</th>
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
                            <td className="action-cell">
                                <button className="btn-edit" onClick={() => handleEdit('clothing', product)}>Edit</button>
                                <button className="btn-delete" onClick={() => handleDelete('clothing', product.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Products;
