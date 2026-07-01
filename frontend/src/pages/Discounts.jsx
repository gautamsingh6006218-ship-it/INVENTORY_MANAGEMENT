import React, { useState, useEffect } from 'react';
import { discountAPI } from '../api/axios';
import ConfirmModal from '../components/ConfirmModal';
import './Discounts.css';

function Discounts() {
    const [discounts, setDiscounts] = useState([]);
    const [showForm, setShowForm] = useState(false);
    const [editingDiscount, setEditingDiscount] = useState(null);
    const [editData, setEditData] = useState({});
    const [error, setError] = useState('');
    const [editError, setEditError] = useState('');
    const [errors, setErrors] = useState({});
    const [editErrors, setEditErrors] = useState({});
    const [pendingDeleteId, setPendingDeleteId] = useState(null);

    // add form fields
    const [code, setCode] = useState('');
    const [discountType, setDiscountType] = useState('percentage');
    const [value, setValue] = useState('');
    const [productId, setProductId] = useState('');
    const [minOrderValue, setMinOrderValue] = useState('');
    const [validFrom, setValidFrom] = useState('');
    const [validUntil, setValidUntil] = useState('');

    const validate = () => {
        const errs = {};
        if (!code.trim()) errs.code = 'Discount code is required';
        if (!value || value <= 0) errs.value = 'Value must be greater than 0';
        if (!validFrom) errs.validFrom = 'Valid from date is required';
        if (!validUntil) errs.validUntil = 'Valid until date is required';
        else if (validFrom && validUntil <= validFrom) errs.validUntil = 'Valid until must be after valid from';
        setErrors(errs);
        return Object.keys(errs).length === 0;
    };

    const validateEdit = () => {
        const errs = {};
        if (!editData.code?.trim()) errs.code = 'Discount code is required';
        if (!editData.value || editData.value <= 0) errs.value = 'Value must be greater than 0';
        if (!editData.valid_from) errs.valid_from = 'Valid from date is required';
        if (!editData.valid_until) errs.valid_until = 'Valid until date is required';
        else if (editData.valid_from && editData.valid_until <= editData.valid_from) errs.valid_until = 'Valid until must be after valid from';
        setEditErrors(errs);
        return Object.keys(errs).length === 0;
    };

    useEffect(() => { fetchDiscounts(); }, []);

    const fetchDiscounts = () => {
        discountAPI.get('/discounts/')
            .then(r => setDiscounts(r.data))
            .catch(console.log);
    };

    const handleAdd = async () => {
        if (!validate()) return;
        setError('');
        try {
            await discountAPI.post('/discounts/', {
                code,
                discount_type: discountType,
                value,
                product_id: productId,
                min_order_value: minOrderValue,
                // backend expects datetime — append T00:00:00Z to make date into datetime
                valid_from: validFrom + 'T00:00:00Z',
                valid_until: validUntil + 'T00:00:00Z',
            });
            fetchDiscounts();
            setCode(''); setDiscountType('percentage'); setValue('');
            setProductId(''); setMinOrderValue(''); setValidFrom(''); setValidUntil('');
            setShowForm(false);
        } catch (err) {
            const data = err.response?.data;
            if (data) {
                const firstError = Object.values(data)[0];
                setError(Array.isArray(firstError) ? firstError[0] : firstError);
            } else { setError('Failed to add discount.'); }
        }
    };

    const handleEdit = (discount) => {
        setEditingDiscount(discount);
        // slice(0, 10) converts ISO datetime to YYYY-MM-DD for the date input
        setEditData({
            ...discount,
            valid_from: discount.valid_from.slice(0, 10),
            valid_until: discount.valid_until.slice(0, 10),
        });
        setEditError('');
        setShowForm(false);
    };

    const handleUpdate = async () => {
        if (!validateEdit()) return;
        setEditError('');
        try {
            await discountAPI.put(`/discounts/${editingDiscount.id}/`, {
                ...editData,
                valid_from: editData.valid_from + 'T00:00:00Z',
                valid_until: editData.valid_until + 'T00:00:00Z',
            });
            fetchDiscounts();
            setEditingDiscount(null);
        } catch (err) {
            const data = err.response?.data;
            if (data) {
                const firstError = Object.values(data)[0];
                setEditError(Array.isArray(firstError) ? firstError[0] : firstError);
            } else { setEditError('Failed to update discount.'); }
        }
    };

    const handleDelete = async (id) => {
        try {
            await discountAPI.delete(`/discounts/${id}/`);
            setDiscounts(discounts.filter(d => d.id !== id));
        } catch (err) { console.log(err); }
    };

    // PATCH /discounts/:id/toggle-active/ — flips is_active without touching other fields
    const handleToggleActive = async (discount) => {
        try {
            await discountAPI.patch(`/discounts/${discount.id}/toggle-active/`, {
                is_active: !discount.is_active,
            });
            setDiscounts(discounts.map(d =>
                d.id === discount.id ? { ...d, is_active: !d.is_active } : d
            ));
        } catch (err) { console.log(err); }
    };

    return (
        <div className="page">
            <div className="page-header">
                <h2>Discounts</h2>
                <button className="btn-primary" onClick={() => { setShowForm(!showForm); setEditingDiscount(null); }}>
                    {showForm ? 'Cancel' : '+ Add Discount'}
                </button>
            </div>

            {/* add discount form */}
            {showForm && (
                <div className="form-card">
                    <h3>Add New Discount</h3>
                    {error && <p className="form-error">{error}</p>}
                    <div className="form-row">
                        <label>Code</label>
                        <input value={code} onChange={e => setCode(e.target.value)} placeholder="e.g. SAVE10" />
                    </div>
                    {errors.code && <p className="field-error">{errors.code}</p>}
                    <div className="form-row">
                        <label>Type</label>
                        <select value={discountType} onChange={e => setDiscountType(e.target.value)}>
                            <option value="percentage">Percentage</option>
                            <option value="fixed">Fixed Amount</option>
                        </select>
                    </div>
                    <div className="form-row">
                        <label>Value</label>
                        <input type="number" value={value} onChange={e => setValue(e.target.value)} placeholder="e.g. 10 for 10% or $10" />
                    </div>
                    {errors.value && <p className="field-error">{errors.value}</p>}
                    <div className="form-row">
                        <label>Product ID</label>
                        <input type="number" value={productId} onChange={e => setProductId(e.target.value)} placeholder="Product ID" />
                    </div>
                    <div className="form-row">
                        <label>Min Order Value</label>
                        <input type="number" value={minOrderValue} onChange={e => setMinOrderValue(e.target.value)} placeholder="Minimum order total" />
                    </div>
                    <div className="form-row">
                        <label>Valid From</label>
                        <input type="date" value={validFrom} onChange={e => setValidFrom(e.target.value)} />
                    </div>
                    {errors.validFrom && <p className="field-error">{errors.validFrom}</p>}
                    <div className="form-row">
                        <label>Valid Until</label>
                        <input type="date" value={validUntil} onChange={e => setValidUntil(e.target.value)} />
                    </div>
                    {errors.validUntil && <p className="field-error">{errors.validUntil}</p>}
                    <button className="btn-submit" onClick={handleAdd}>Add Discount</button>
                </div>
            )}

            {/* edit discount form */}
            {editingDiscount && (
                <div className="form-card">
                    <h3>Edit Discount</h3>
                    {editError && <p className="form-error">{editError}</p>}
                    <div className="form-row">
                        <label>Code</label>
                        <input value={editData.code || ''} onChange={e => setEditData({ ...editData, code: e.target.value })} />
                    </div>
                    {editErrors.code && <p className="field-error">{editErrors.code}</p>}
                    <div className="form-row">
                        <label>Type</label>
                        <select value={editData.discount_type || 'percentage'} onChange={e => setEditData({ ...editData, discount_type: e.target.value })}>
                            <option value="percentage">Percentage</option>
                            <option value="fixed">Fixed Amount</option>
                        </select>
                    </div>
                    <div className="form-row">
                        <label>Value</label>
                        <input type="number" value={editData.value || ''} onChange={e => setEditData({ ...editData, value: e.target.value })} />
                    </div>
                    {editErrors.value && <p className="field-error">{editErrors.value}</p>}
                    <div className="form-row">
                        <label>Product ID</label>
                        <input type="number" value={editData.product_id || ''} onChange={e => setEditData({ ...editData, product_id: e.target.value })} />
                    </div>
                    <div className="form-row">
                        <label>Min Order Value</label>
                        <input type="number" value={editData.min_order_value || ''} onChange={e => setEditData({ ...editData, min_order_value: e.target.value })} />
                    </div>
                    <div className="form-row">
                        <label>Valid From</label>
                        <input type="date" value={editData.valid_from || ''} onChange={e => setEditData({ ...editData, valid_from: e.target.value })} />
                    </div>
                    {editErrors.valid_from && <p className="field-error">{editErrors.valid_from}</p>}
                    <div className="form-row">
                        <label>Valid Until</label>
                        <input type="date" value={editData.valid_until || ''} onChange={e => setEditData({ ...editData, valid_until: e.target.value })} />
                    </div>
                    {editErrors.valid_until && <p className="field-error">{editErrors.valid_until}</p>}
                    <div className="form-actions">
                        <button className="btn-submit" onClick={handleUpdate}>Save Changes</button>
                        <button className="btn-cancel" onClick={() => setEditingDiscount(null)}>Cancel</button>
                    </div>
                </div>
            )}

            <table className="data-table">
                <thead>
                    <tr>
                        <th>Code</th>
                        <th>Type</th>
                        <th>Value</th>
                        <th>Product ID</th>
                        <th>Min Order</th>
                        <th>Valid From</th>
                        <th>Valid Until</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {discounts.map(d => (
                        <tr key={d.id}>
                            <td className="code-cell">{d.code}</td>
                            {/* show % or $ symbol based on discount type */}
                            <td>{d.discount_type === 'percentage' ? 'Percentage' : 'Fixed'}</td>
                            <td>{d.discount_type === 'percentage' ? `${d.value}%` : `$${d.value}`}</td>
                            <td>{d.product_id}</td>
                            <td>${d.min_order_value}</td>
                            <td>{d.valid_from.slice(0, 10)}</td>
                            <td>{d.valid_until.slice(0, 10)}</td>
                            <td>
                                <button
                                    className={d.is_active ? 'badge-active' : 'badge-inactive'}
                                    onClick={() => handleToggleActive(d)}
                                >
                                    {d.is_active ? 'Active' : 'Inactive'}
                                </button>
                            </td>
                            <td className="action-cell">
                                <button className="btn-edit" onClick={() => handleEdit(d)}>Edit</button>
                                <button className="btn-delete" onClick={() => setPendingDeleteId(d.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        {pendingDeleteId && (
            <ConfirmModal
                message="Delete this discount? This cannot be undone."
                onConfirm={() => { handleDelete(pendingDeleteId); setPendingDeleteId(null); }}
                onCancel={() => setPendingDeleteId(null)}
            />
        )}
        </div>
    );
}

export default Discounts;
