import React, { useState, useEffect } from 'react';
import { supplierAPI } from '../api/axios';
import './Suppliers.css';

function Suppliers() {
    const [suppliers, setSuppliers] = useState([]);
    const [showForm, setShowForm] = useState(false);
    const [editingSupplier, setEditingSupplier] = useState(null);
    const [editData, setEditData] = useState({});
    const [error, setError] = useState('');
    const [editError, setEditError] = useState('');

    // add form fields
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [phone, setPhone] = useState('');
    const [address, setAddress] = useState('');
    const [productId, setProductId] = useState('');
    const [supplyTimeDays, setSupplyTimeDays] = useState('');
    const [transportMode, setTransportMode] = useState('Road');
    const [rating, setRating] = useState('');

    useEffect(() => { fetchSuppliers(); }, []);

    const fetchSuppliers = () => {
        supplierAPI.get('/suppliers/')
            .then(r => setSuppliers(r.data))
            .catch(console.log);
    };

    const handleAdd = async () => {
        setError('');
        try {
            await supplierAPI.post('/suppliers/', {
                name, email, phone, address,
                product_id: productId,
                supply_time_days: supplyTimeDays,
                transport_mode: transportMode,
                rating,
            });
            fetchSuppliers();
            setName(''); setEmail(''); setPhone(''); setAddress('');
            setProductId(''); setSupplyTimeDays(''); setTransportMode('Road'); setRating('');
            setShowForm(false);
        } catch (err) {
            const data = err.response?.data;
            if (data) {
                const firstError = Object.values(data)[0];
                setError(Array.isArray(firstError) ? firstError[0] : firstError);
            } else { setError('Failed to add supplier.'); }
        }
    };

    const handleEdit = (supplier) => {
        setEditingSupplier(supplier);
        setEditData({ ...supplier });
        setEditError('');
        setShowForm(false);
    };

    // PUT /suppliers/:id/ — updates all fields
    const handleUpdate = async () => {
        setEditError('');
        try {
            await supplierAPI.put(`/suppliers/${editingSupplier.id}/`, editData);
            fetchSuppliers();
            setEditingSupplier(null);
        } catch (err) {
            const data = err.response?.data;
            if (data) {
                const firstError = Object.values(data)[0];
                setEditError(Array.isArray(firstError) ? firstError[0] : firstError);
            } else { setEditError('Failed to update supplier.'); }
        }
    };

    const handleDelete = async (id) => {
        try {
            await supplierAPI.delete(`/suppliers/${id}/`);
            setSuppliers(suppliers.filter(s => s.id !== id));
        } catch (err) { console.log(err); }
    };

    // PATCH /suppliers/:id/toggle-active/ — flips is_active without touching other fields
    const handleToggleActive = async (supplier) => {
        try {
            await supplierAPI.patch(`/suppliers/${supplier.id}/toggle-active/`, {
                is_active: !supplier.is_active,
            });
            setSuppliers(suppliers.map(s =>
                s.id === supplier.id ? { ...s, is_active: !s.is_active } : s
            ));
        } catch (err) { console.log(err); }
    };

    const field = (label, value, onChange, type = 'text', placeholder = '') => (
        <div className="form-row">
            <label>{label}</label>
            <input type={type} value={value} onChange={onChange} placeholder={placeholder} />
        </div>
    );

    return (
        <div className="page">
            <div className="page-header">
                <h2>Suppliers</h2>
                <button className="btn-primary" onClick={() => { setShowForm(!showForm); setEditingSupplier(null); }}>
                    {showForm ? 'Cancel' : '+ Add Supplier'}
                </button>
            </div>

            {/* add supplier form */}
            {showForm && (
                <div className="form-card">
                    <h3>Add New Supplier</h3>
                    {error && <p className="form-error">{error}</p>}
                    {field('Name', name, e => setName(e.target.value), 'text', 'Supplier name')}
                    {field('Email', email, e => setEmail(e.target.value), 'email', 'supplier@email.com')}
                    {field('Phone', phone, e => setPhone(e.target.value), 'text', 'Phone number')}
                    {field('Address', address, e => setAddress(e.target.value), 'text', 'Full address')}
                    {field('Product ID', productId, e => setProductId(e.target.value), 'number', 'Product ID')}
                    {field('Supply Time (days)', supplyTimeDays, e => setSupplyTimeDays(e.target.value), 'number', 'e.g. 7')}
                    <div className="form-row">
                        <label>Transport Mode</label>
                        <select value={transportMode} onChange={e => setTransportMode(e.target.value)}>
                            <option value="Road">Road</option>
                            <option value="Air">Air</option>
                            <option value="Sea">Sea</option>
                            <option value="Rail">Rail</option>
                        </select>
                    </div>
                    {field('Rating', rating, e => setRating(e.target.value), 'number', '1.0 – 5.0')}
                    <button className="btn-submit" onClick={handleAdd}>Add Supplier</button>
                </div>
            )}

            {/* edit supplier form — pre-filled with selected supplier's data */}
            {editingSupplier && (
                <div className="form-card">
                    <h3>Edit Supplier</h3>
                    {editError && <p className="form-error">{editError}</p>}
                    {[
                        ['Name', 'name'], ['Email', 'email'], ['Phone', 'phone'],
                        ['Address', 'address'], ['Product ID', 'product_id'],
                        ['Supply Time (days)', 'supply_time_days'], ['Rating', 'rating'],
                    ].map(([label, key]) => (
                        <div className="form-row" key={key}>
                            <label>{label}</label>
                            <input
                                value={editData[key] || ''}
                                onChange={e => setEditData({ ...editData, [key]: e.target.value })}
                            />
                        </div>
                    ))}
                    <div className="form-row">
                        <label>Transport Mode</label>
                        <select value={editData.transport_mode || 'Road'} onChange={e => setEditData({ ...editData, transport_mode: e.target.value })}>
                            <option value="Road">Road</option>
                            <option value="Air">Air</option>
                            <option value="Sea">Sea</option>
                            <option value="Rail">Rail</option>
                        </select>
                    </div>
                    <div className="form-actions">
                        <button className="btn-submit" onClick={handleUpdate}>Save Changes</button>
                        <button className="btn-cancel" onClick={() => setEditingSupplier(null)}>Cancel</button>
                    </div>
                </div>
            )}

            <table className="data-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Product ID</th>
                        <th>Supply (days)</th>
                        <th>Transport</th>
                        <th>Rating</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {suppliers.map(s => (
                        <tr key={s.id}>
                            <td>{s.name}</td>
                            <td>{s.email}</td>
                            <td>{s.phone}</td>
                            <td>{s.product_id}</td>
                            <td>{s.supply_time_days}d</td>
                            <td>{s.transport_mode}</td>
                            <td>{s.rating}</td>
                            <td>
                                {/* toggle button flips is_active via PATCH — no full page reload */}
                                <button
                                    className={s.is_active ? 'badge-active' : 'badge-inactive'}
                                    onClick={() => handleToggleActive(s)}
                                >
                                    {s.is_active ? 'Active' : 'Inactive'}
                                </button>
                            </td>
                            <td className="action-cell">
                                <button className="btn-edit" onClick={() => handleEdit(s)}>Edit</button>
                                <button className="btn-delete" onClick={() => handleDelete(s.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Suppliers;
