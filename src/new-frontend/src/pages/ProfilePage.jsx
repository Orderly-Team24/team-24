import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/App.css';

const API_URL = 'https://team-24-1.onrender.com';

function ProfilePage() {
  const navigate = useNavigate();
  const [likes, setLikes] = useState('');
  const [dislikes, setDislikes] = useState('');
  const [allergies, setAllergies] = useState('');
  const [loadError, setLoadError] = useState('');
  const [saveError, setSaveError] = useState('');
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [deleteError, setDeleteError] = useState('');

  const token = localStorage.getItem('orderly_access_token');

  const parseList = (value) =>
    value.split(',').map(item => item.trim()).filter(Boolean);

  const listToString = (arr) => (arr || []).join(', ');

  useEffect(() => {
    const fetchPreferences = async () => {
      try {
        const response = await fetch(`${API_URL}/users/me/preferences`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!response.ok) {
          setLoadError('Failed to load preferences.');
          return;
        }
        const data = await response.json();
        setLikes(listToString(data.likes));
        setDislikes(listToString(data.dislikes));
        setAllergies(listToString(data.allergies));
      } catch (err) {
        setLoadError('Something went wrong loading your preferences.');
      }
    };

    fetchPreferences();
  }, [token]);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaveError('');
    setSaveSuccess(false);

    try {
      const response = await fetch(`${API_URL}/users/me/preferences`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          cuisine: null,
          likes: parseList(likes),
          dislikes: parseList(dislikes),
          allergies: parseList(allergies),
        }),
      });

      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        setSaveError(body.detail || 'Failed to save preferences.');
        return;
      }

      setSaveSuccess(true);
    } catch (err) {
      setSaveError('Something went wrong. Please try again.');
    }
  };

  const handleDelete = async () => {
    try {
      const response = await fetch(`${API_URL}/users/me`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        setDeleteError(body.detail || 'Failed to delete account. Please try again.');
        return;
      }

      localStorage.removeItem('orderly_access_token');
      localStorage.removeItem('orderly_refresh_token');
      localStorage.removeItem('orderly_menu');
      localStorage.removeItem('orderly_preferences');
      localStorage.removeItem('orderly_budget');
      navigate('/register');
    } catch (err) {
      setDeleteError('Something went wrong. Please try again.');
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-container" style={{ maxWidth: 600 }}>
        <h2>Profile</h2>
        <p className="subtitle">View and edit your food preferences</p>

        {loadError && <div className="message error">{loadError}</div>}

        <form onSubmit={handleSave} className="preferences-form">
          <div className="form-group">
            <label className="form-label">Allergies <span className="optional">(optional)</span></label>
            <p className="hint">Enter ingredients you're allergic to, separated by commas</p>
            <input
              type="text"
              className="form-select"
              placeholder="e.g. Nuts, Gluten, Shellfish"
              value={allergies}
              onChange={(e) => setAllergies(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Dislikes <span className="optional">(optional)</span></label>
            <p className="hint">Enter ingredients you don't like, separated by commas</p>
            <input
              type="text"
              className="form-select"
              placeholder="e.g. Mushrooms, Onion"
              value={dislikes}
              onChange={(e) => setDislikes(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Likes <span className="optional">(optional)</span></label>
            <p className="hint">Enter ingredients you particularly enjoy, separated by commas</p>
            <input
              type="text"
              className="form-select"
              placeholder="e.g. Chicken, Garlic, Tomatoes"
              value={likes}
              onChange={(e) => setLikes(e.target.value)}
            />
          </div>

          {saveError && <div className="message error">{saveError}</div>}
          {saveSuccess && <div className="message info">Preferences saved successfully!</div>}

          <div className="form-actions">
            <button type="submit" className="submit-btn">Save preferences</button>
          </div>
        </form>

        <div style={{ marginTop: 48, borderTop: '1px solid #e2e8f0', paddingTop: 32 }}>
          {!showConfirm ? (
            <button className="remove-btn" onClick={() => setShowConfirm(true)}>
              Delete account
            </button>
          ) : (
            <div>
              <p style={{ color: '#e53e3e', fontWeight: 600 }}>This action is irreversible. All your data will be permanently deleted.</p>
              <p>Are you sure you want to delete your account?</p>
              <div style={{ display: 'flex', gap: 12, justifyContent: 'center', marginTop: 16 }}>
                <button className="remove-btn" onClick={handleDelete}>Yes, delete my account</button>
                <button className="submit-btn" onClick={() => setShowConfirm(false)}>Cancel</button>
              </div>
            </div>
          )}
          {deleteError && <div className="message error" style={{ marginTop: 16 }}>{deleteError}</div>}
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;
