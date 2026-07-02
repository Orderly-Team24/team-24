import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/App.css';

const API_URL = 'https://team-24.onrender.com';

function ProfilePage() {
  const navigate = useNavigate();
  const [showConfirm, setShowConfirm] = useState(false);
  const [error, setError] = useState('');

  const handleDelete = async () => {
    const token = localStorage.getItem('orderly_access_token');

    try {
      const response = await fetch(`${API_URL}/users/me`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        setError(body.detail || 'Failed to delete account. Please try again.');
        return;
      }

      localStorage.removeItem('orderly_access_token');
      localStorage.removeItem('orderly_refresh_token');
      localStorage.removeItem('orderly_menu');
      localStorage.removeItem('orderly_preferences');
      localStorage.removeItem('orderly_budget');
      navigate('/register');
    } catch (err) {
      setError('Something went wrong. Please try again.');
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-container" style={{ maxWidth: 440, textAlign: 'center' }}>
        <h2>Profile</h2>

        {!showConfirm ? (
          <button
            className="remove-btn"
            onClick={() => setShowConfirm(true)}
            style={{ marginTop: 32 }}
          >
            Delete account
          </button>
        ) : (
          <div style={{ marginTop: 32 }}>
            <p style={{ color: '#e53e3e', fontWeight: 600 }}>This action is irreversible. All your data will be permanently deleted.</p>
            <p>Are you sure you want to delete your account?</p>
            <div style={{ display: 'flex', gap: 12, justifyContent: 'center', marginTop: 16 }}>
              <button className="remove-btn" onClick={handleDelete}>Yes, delete my account</button>
              <button className="submit-btn" onClick={() => setShowConfirm(false)}>Cancel</button>
            </div>
          </div>
        )}

        {error && <div className="message error" style={{ marginTop: 16 }}>{error}</div>}
      </div>
    </div>
  );
}

export default ProfilePage;