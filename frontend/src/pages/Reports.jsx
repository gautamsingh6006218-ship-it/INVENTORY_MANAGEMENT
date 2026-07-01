            import React, { useState, useEffect } from 'react';
import { reportAPI } from '../api/axios';
import ConfirmModal from '../components/ConfirmModal';
import './Reports.css';

function Reports() {
    const [reports, setReports] = useState([]);
    const [showForm, setShowForm] = useState(false);
    const [viewingReport, setViewingReport] = useState(null);

    // form fields
    const [reportType, setReportType] = useState('sales');
    const [reportStatus, setReportStatus] = useState('pending');
    const [createdBy, setCreatedBy] = useState('');
    const [dataInput, setDataInput] = useState('');
    const [error, setError] = useState('');
    const [errors, setErrors] = useState({});

    useEffect(() => {
        fetchReports();
        // decode JWT to pre-fill created_by with the logged-in user's ID
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const payload = JSON.parse(atob(token.split('.')[1]));
                // SimpleJWT puts user_id in the token payload
                setCreatedBy(payload.user_id || '');
            } catch { }
        }
    }, []);

    const fetchReports = () => {
        reportAPI.get('/reports/')
            .then(r => setReports(r.data))
            .catch(console.log);
    };

    const handleGenerate = async () => {
        const errs = {};
        if (!createdBy) errs.createdBy = 'User ID is required';
        setErrors(errs);
        if (Object.keys(errs).length > 0) return;

        setError('');
        // data field must be valid JSON — parse it before sending
        let parsedData;
        try {
            parsedData = dataInput.trim() ? JSON.parse(dataInput) : {};
        } catch {
            setError('Data must be valid JSON. Example: {"total": 100}');
            return;
        }

        try {
            await reportAPI.post('/reports/', {
                report_type: reportType,
                status: reportStatus,
                data: parsedData,
                created_by: createdBy,
            });
            fetchReports();
            setDataInput('');
            setReportType('sales');
            setReportStatus('pending');
            setShowForm(false);
        } catch (err) {
            const data = err.response?.data;
            if (data) {
                const firstError = Object.values(data)[0];
                setError(Array.isArray(firstError) ? firstError[0] : firstError);
            } else { setError('Failed to generate report.'); }
        }
    };

    // DELETE /reports/:id/ — removes the report permanently
    const handleDelete = async (id) => {
        try {
            await reportAPI.delete(`/reports/${id}/`);
            setReports(reports.filter(r => r.id !== id));
            // close the viewer if the deleted report was open
            if (viewingReport?.id === id) setViewingReport(null);
        } catch (err) { console.log(err); }
    };

    // formats the JSON data field for readable display
    const formatData = (data) => JSON.stringify(data, null, 2);

    return (
        <div className="page">
            <div className="page-header">
                <h2>Reports</h2>
                <button className="btn-primary" onClick={() => { setShowForm(!showForm); setViewingReport(null); }}>
                    {showForm ? 'Cancel' : '+ Generate Report'}
                </button>
            </div>

            {/* generate report form */}
            {showForm && (
                <div className="form-card">
                    <h3>Generate New Report</h3>
                    {error && <p className="form-error">{error}</p>}

                    <div className="form-row">
                        <label>Report Type</label>
                        <select value={reportType} onChange={e => setReportType(e.target.value)}>
                            <option value="sales">Sales</option>
                            <option value="inventory">Inventory</option>
                            <option value="orders">Orders</option>
                        </select>
                    </div>
                    <div className="form-row">
                        <label>Status</label>
                        <select value={reportStatus} onChange={e => setReportStatus(e.target.value)}>
                            <option value="pending">Pending</option>
                            <option value="completed">Completed</option>
                            <option value="failed">Failed</option>
                        </select>
                    </div>
                    <div className="form-row">
                        <label>Created By (User ID)</label>
                        <input
                            type="number"
                            value={createdBy}
                            onChange={e => setCreatedBy(e.target.value)}
                            placeholder="User ID"
                        />
                    </div>
                    {errors.createdBy && <p className="field-error">{errors.createdBy}</p>}
                    <div className="form-row form-row--top">
                        <label>Data (JSON)</label>
                        {/* textarea for JSON input — backend stores this in a JSONField */}
                        <textarea
                            value={dataInput}
                            onChange={e => setDataInput(e.target.value)}
                            placeholder={'{\n  "total_sales": 5000,\n  "period": "June 2026"\n}'}
                            rows={5}
                        />
                    </div>

                    <button className="btn-submit" onClick={handleGenerate}>Generate</button>
                </div>
            )}

            {/* report data viewer — shown when View is clicked on a row */}
            {viewingReport && (
                <div className="data-viewer">
                    <div className="data-viewer-header">
                        <h3>{viewingReport.report_type.charAt(0).toUpperCase() + viewingReport.report_type.slice(1)} Report #{viewingReport.id}</h3>
                        <button className="btn-close" onClick={() => setViewingReport(null)}>✕ Close</button>
                    </div>
                    {/* pre tag preserves the JSON indentation from formatData() */}
                    <pre className="data-content">{formatData(viewingReport.data)}</pre>
                </div>
            )}

            {/* reports table */}
            {reports.length === 0 ? (
                <p className="empty-state">No reports yet. Generate one above.</p>
            ) : (
                <table className="reports-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Type</th>
                            <th>Status</th>
                            <th>Created By</th>
                            <th>Generated At</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {reports.map(r => (
                            <tr key={r.id}>
                                <td>#{r.id}</td>
                                <td>
                                    <span className={`type-badge type-${r.report_type}`}>
                                        {r.report_type.charAt(0).toUpperCase() + r.report_type.slice(1)}
                                    </span>
                                </td>
                                <td>
                                    <span className={`status-badge status-${r.status}`}>
                                        {r.status.charAt(0).toUpperCase() + r.status.slice(1)}
                                    </span>
                                </td>
                                <td>User #{r.created_by}</td>
                                <td>{r.generated_at.slice(0, 10)}</td>
                                <td className="action-cell">
                                    {/* View opens the data viewer panel above the table */}
                                    <button
                                        className="btn-view"
                                        onClick={() => setViewingReport(viewingReport?.id === r.id ? null : r)}
                                    >
                                        {viewingReport?.id === r.id ? 'Hide' : 'View'}
                                    </button>
                                    <button className="btn-delete" onClick={() => handleDelete(r.id)}>Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default Reports;
