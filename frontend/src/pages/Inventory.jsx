import React, { useState, useEffect } from 'react';
import { inventoryAPI } from '../api/axios';
import './Inventory.css';

function Inventory() {
    const [stock, setStock] = useState([]);

    // controls the "create new stock entry" form
    const [showForm, setShowForm] = useState(false);
    const [productId, setProductId] = useState('');
    const [quantity, setQuantity] = useState('');
    const [warehouseLocation, setWarehouseLocation] = useState('');
    const [reorderLevel, setReorderLevel] = useState(10);
    const [addError, setAddError] = useState('');

    // tracks which stock entry the user is adjusting and whether they're adding or reducing
    const [adjustingItem, setAdjustingItem] = useState(null);
    const [adjustMode, setAdjustMode] = useState(''); // 'add' or 'reduce'
    const [adjustQty, setAdjustQty] = useState('');
    const [adjustError, setAdjustError] = useState('');

    useEffect(() => { fetchStock(); }, []);

    const fetchStock = () => {
        inventoryAPI.get('/')
            .then(r => setStock(r.data))
            .catch(console.log);
    };

    // POST / — creates a brand new stock record for a product
    const handleCreateStock = async () => {
        setAddError('');
        try {
            await inventoryAPI.post('/', {
                product_id: productId,
                quantity,
                warehouse_location: warehouseLocation,
                reorder_level: reorderLevel,
            });
            fetchStock();
            setProductId(''); setQuantity(''); setWarehouseLocation(''); setReorderLevel(10);
            setShowForm(false);
        } catch (err) {
            const data = err.response?.data;
            if (data) {
                const firstError = Object.values(data)[0];
                setAddError(Array.isArray(firstError) ? firstError[0] : firstError);
            } else { setAddError('Failed to create stock entry.'); }
        }
    };

    // opens the adjust panel for the clicked row
    const openAdjust = (item, mode) => {
        setAdjustingItem(item);
        setAdjustMode(mode);
        setAdjustQty('');
        setAdjustError('');
        setShowForm(false);
    };

    // PUT /:id/add-stock/ — adds units to existing quantity, fires stock.added Kafka event
    // PUT /:id/reduce-stock/ — subtracts units, fires stock.low event if below reorder_level
    const handleAdjust = async () => {
        setAdjustError('');
        const endpoint = adjustMode === 'add'
            ? `/${adjustingItem.id}/add-stock/`
            : `/${adjustingItem.id}/reduce-stock/`;
        try {
            await inventoryAPI.put(endpoint, { quantity: adjustQty });
            fetchStock();
            setAdjustingItem(null);
            setAdjustQty('');
        } catch (err) {
            const data = err.response?.data;
            // reduce-stock returns { error: 'Insufficient quantity' } if qty > current stock
            setAdjustError(data?.error || 'Failed to adjust stock.');
        }
    };

    // DELETE /:id/ — removes the stock record entirely
    const handleDelete = async (id) => {
        try {
            await inventoryAPI.delete(`/${id}/`);
            setStock(stock.filter(s => s.id !== id));
        } catch (err) { console.log(err); }
    };

    return (
        <div className="page">
            <div className="page-header">
                <h2>Inventory</h2>
                <button className="btn-primary" onClick={() => { setShowForm(!showForm); setAdjustingItem(null); }}>
                    {showForm ? 'Cancel' : '+ Add Stock Entry'}
                </button>
            </div>

            {/* create new stock entry form */}
            {showForm && (
                <div className="form-card">
                    <h3>New Stock Entry</h3>
                    {addError && <p className="form-error">{addError}</p>}
                    <div className="form-row">
                        <label>Product ID</label>
                        <input type="number" value={productId} onChange={e => setProductId(e.target.value)} placeholder="Product ID" />
                    </div>
                    <div className="form-row">
                        <label>Quantity</label>
                        <input type="number" value={quantity} onChange={e => setQuantity(e.target.value)} placeholder="Initial stock count" />
                    </div>
                    <div className="form-row">
                        <label>Warehouse Location</label>
                        <input value={warehouseLocation} onChange={e => setWarehouseLocation(e.target.value)} placeholder="e.g. Aisle 3, Shelf B" />
                    </div>
                    <div className="form-row">
                        <label>Reorder Level</label>
                        <input type="number" value={reorderLevel} onChange={e => setReorderLevel(e.target.value)} placeholder="Alert threshold" />
                    </div>
                    <button className="btn-submit" onClick={handleCreateStock}>Create</button>
                </div>
            )}

            {/* adjust stock panel — shown when Add or Reduce is clicked on a row */}
            {adjustingItem && (
                <div className={`form-card ${adjustMode === 'add' ? 'form-card--add' : 'form-card--reduce'}`}>
                    <h3>
                        {/* title changes based on mode */}
                        {adjustMode === 'add' ? '+ Add Stock' : '- Reduce Stock'} — Product #{adjustingItem.product_id}
                    </h3>
                    <p className="adjust-current">Current quantity: <strong>{adjustingItem.quantity}</strong></p>
                    {adjustError && <p className="form-error">{adjustError}</p>}
                    <div className="form-row">
                        <label>Quantity</label>
                        <input
                            type="number"
                            value={adjustQty}
                            onChange={e => setAdjustQty(e.target.value)}
                            placeholder="Units to add/remove"
                            autoFocus
                        />
                    </div>
                    <div className="form-actions">
                        <button
                            className={adjustMode === 'add' ? 'btn-add' : 'btn-reduce'}
                            onClick={handleAdjust}
                        >
                            {adjustMode === 'add' ? 'Add Stock' : 'Reduce Stock'}
                        </button>
                        <button className="btn-cancel" onClick={() => setAdjustingItem(null)}>Cancel</button>
                    </div>
                </div>
            )}

            <table className="inventory-table">
                <thead>
                    <tr>
                        <th>Product ID</th>
                        <th>Quantity</th>
                        <th>Warehouse Location</th>
                        <th>Reorder Level</th>
                        <th>Last Updated</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {stock.map(item => (
                        <tr key={item.id}>
                            <td>{item.product_id}</td>
                            <td>
                                {/* red if at or below reorder level — signals restock needed */}
                                <span className={item.quantity <= item.reorder_level ? 'low-stock' : ''}>
                                    {item.quantity}
                                </span>
                            </td>
                            <td>{item.warehouse_location}</td>
                            <td>{item.reorder_level}</td>
                            <td>{item.last_updated.slice(0, 10)}</td>
                            <td className="action-cell">
                                {/* Add calls PUT /:id/add-stock/ — fires stock.added Kafka event */}
                                <button className="btn-add-sm" onClick={() => openAdjust(item, 'add')}>+ Add</button>
                                {/* Reduce calls PUT /:id/reduce-stock/ — fires stock.low if below reorder_level */}
                                <button className="btn-reduce-sm" onClick={() => openAdjust(item, 'reduce')}>- Reduce</button>
                                <button className="btn-delete" onClick={() => handleDelete(item.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default Inventory;
