import React, { useState, useEffect } from 'react';
import { userAPI } from '../api/axios';
import { useNavigate } from 'react-router-dom';
import './Profile.css';

function Profile() {
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    // GET /profile/ — backend reads the JWT token from the Authorization header and returns user details
    useEffect(() => {
        userAPI.get('/profile/')
            .then(response => setUser(response.data.user))
            .catch(err => console.log(err));
    }, []);

    const handleLogout = async () => {
        try {
            const refresh = localStorage.getItem('refresh');
            await userAPI.post('/logout/', { refresh });
        } catch (err) {}
        localStorage.removeItem('token');
        localStorage.removeItem('refresh');
        navigate('/');
    };

    // generates initials from username — e.g. "john_doe" → "JD", "alice" → "A"
    const getInitials = (username) => {
        if (!username) return '?';
        return username
            .split(/[\s_-]/)
            .map(word => word[0]?.toUpperCase())
            .join('')
            .slice(0, 2);
    };

    // format role text — e.g. "admin" → "Admin"
    const formatRole = (role) => role ? role.charAt(0).toUpperCase() + role.slice(1) : '';

    if (!user) return <div className="profile-page"><p className="loading">Loading profile...</p></div>;

    return (
        <div className="profile-page">
            <h2>Profile</h2>

            <div className="profile-card">
                {/* avatar circle with user initials — no image needed */}
                <div className="avatar">{getInitials(user.username)}</div>

                <div className="profile-info">
                    <h3 className="profile-name">{user.username}</h3>
                    {/* role badge — colour matches the role type */}
                    <span className={`role-badge role-${user.role}`}>{formatRole(user.role)}</span>
                </div>
            </div>

            {/* detail rows — label on left, value on right */}
            <div className="detail-card">
                <div className="detail-row">
                    <span className="detail-label">Email</span>
                    <span className="detail-value">{user.email}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Phone</span>
                    <span className="detail-value">{user.phone || '—'}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Role</span>
                    <span className="detail-value">{formatRole(user.role)}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">Member Since</span>
                    {/* slice(0, 10) extracts YYYY-MM-DD from the ISO datetime string */}
                    <span className="detail-value">{user.created_at.slice(0, 10)}</span>
                </div>
                <div className="detail-row">
                    <span className="detail-label">User ID</span>
                    <span className="detail-value">#{user.id}</span>
                </div>
            </div>

            <button className="btn-logout" onClick={handleLogout}>Logout</button>
        </div>
    );
}

export default Profile;
