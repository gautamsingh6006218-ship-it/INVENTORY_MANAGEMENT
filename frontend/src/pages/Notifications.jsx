import React, { useState, useEffect } from 'react';
import { notificationAPI } from '../api/axios';
import ConfirmModal from '../components/ConfirmModal';
import './Notifications.css';

function Notifications() {
    const [notifications, setNotifications] = useState([]);
    const [pendingDeleteId, setPendingDeleteId] = useState(null);

    useEffect(() => {
        notificationAPI.get('/')
            .then(response => setNotifications(response.data))
            .catch(err => console.log(err));
    }, []);

    // PATCH /notifications/:id/mark-read/ — flips is_read for one notification
    const handleMarkRead = async (id, value) => {
        try {
            await notificationAPI.patch(`/${id}/mark-read/`, { is_read: value });
            // update local state directly so UI reflects change without a full refetch
            setNotifications(notifications.map(n =>
                n.id === id ? { ...n, is_read: value } : n
            ));
        } catch (err) { console.log(err); }
    };

    // mark every unread notification as read in one go
    const handleMarkAllRead = async () => {
        const unread = notifications.filter(n => !n.is_read);
        // fire all PATCH requests in parallel using Promise.all
        await Promise.all(unread.map(n =>
            notificationAPI.patch(`/${n.id}/mark-read/`, { is_read: true })
        ));
        setNotifications(notifications.map(n => ({ ...n, is_read: true })));
    };

    // DELETE /notifications/:id/ — removes the notification permanently
    const handleDelete = async (id) => {
        try {
            await notificationAPI.delete(`/${id}/`);
            setNotifications(notifications.filter(n => n.id !== id));
        } catch (err) { console.log(err); }
    };

    const unreadCount = notifications.filter(n => !n.is_read).length;

    return (
        <div className="page">
            <div className="page-header">
                <div className="header-left">
                    <h2>Notifications</h2>
                    {/* show unread count badge next to title when there are unread items */}
                    {unreadCount > 0 && (
                        <span className="unread-badge">{unreadCount} unread</span>
                    )}
                </div>
                {/* only show button when there are unread notifications */}
                {unreadCount > 0 && (
                    <button className="btn-mark-all" onClick={handleMarkAllRead}>
                        Mark All as Read
                    </button>
                )}
            </div>

            {notifications.length === 0 && (
                <p className="empty-state">No notifications yet.</p>
            )}

            {notifications.map(n => (
                <div key={n.id} className={`notif-card ${!n.is_read ? 'notif-card--unread' : ''}`}>
                    <div className="notif-body">
                        <p className="notif-message">{n.message}</p>
                        {/* show read/unread as a small tag */}
                        <span className={`notif-tag ${n.is_read ? 'tag-read' : 'tag-unread'}`}>
                            {n.is_read ? 'Read' : 'Unread'}
                        </span>
                    </div>
                    <div className="notif-actions">
                        {/* toggle between mark as read / mark as unread */}
                        {n.is_read ? (
                            <button className="btn-unread" onClick={() => handleMarkRead(n.id, false)}>
                                Mark as Unread
                            </button>
                        ) : (
                            <button className="btn-read" onClick={() => handleMarkRead(n.id, true)}>
                                Mark as Read
                            </button>
                        )}
                        <button className="btn-delete" onClick={() => setPendingDeleteId(n.id)}>
                            Delete
                        </button>
                    </div>
                </div>
            ))}
        {pendingDeleteId && (
            <ConfirmModal
                message="Delete this notification? This cannot be undone."
                onConfirm={() => { handleDelete(pendingDeleteId); setPendingDeleteId(null); }}
                onCancel={() => setPendingDeleteId(null)}
            />
        )}
        </div>
    );
}

export default Notifications;
