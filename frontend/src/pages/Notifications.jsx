import React, { useState, useEffect } from 'react';
import { notificationAPI } from '../api/axios';
import './Notifications.css';

function Notifications() {
    // holds array of notifications fetched from notification-service
    const [notifications, setNotifications] = useState([]);

    // runs once on page load — fetches all notifications from notification-service
    useEffect(() => {
        notificationAPI.get('/')
            .then(response => setNotifications(response.data))
            .catch(error => console.log(error));
    }, []);

    return (
        <div className="page">
            <h2>Notifications</h2>
            {/* unread notifications get extra border-left styling from .card.unread in CSS */}
            {notifications.map(notification => (
                <div className={notification.is_read ? 'card' : 'card unread'} key={notification.id}>
                    <p>{notification.message} — {notification.is_read ? 'Read' : 'Unread'}</p>
                </div>
            ))}
        </div>
    );
}
                    
export default Notifications;