import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/App.css';

const API_URL = 'https://team-24.onrender.com';

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('orderly_access_token');
    if (token) navigate('/upload');
  }, [navigate]);

  const validate = () => {
    const newErrors = {};
    if (!email) {
      newErrors.email = 'Email is required.';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'Please enter a valid email address.';
    }
    if (!password) {
      newErrors.password = 'Password is required.';
    }
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validate();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    setErrors({});
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        setErrors({ server: body.detail || 'Invalid email or password.' });
        return;
      }

      const data = await response.json();
      
      localStorage.setItem('orderly_access_token', data.access_token);
      localStorage.setItem('orderly_refresh_token', data.refresh_token);
      localStorage.setItem("userId", data.user_id);

      // Existing accounts already have preferences saved from signup/profile —
      // pull them into the cache FoodRecommenderPage reads from, so we can
      // skip the questionnaire entirely instead of asking again.
      try {
        const prefsResponse = await fetch(`${API_URL}/users/me/preferences`, {
          headers: { Authorization: `Bearer ${data.access_token}` },
        });
        if (prefsResponse.ok) {
          const prefs = await prefsResponse.json();
          localStorage.setItem('orderly_preferences', JSON.stringify(prefs));
        }
      } catch (_) {
        // Non-fatal — recommendations just fall back to no preferences.
      }

      navigate('/upload');
    } catch (err) {
      setErrors({ server: 'Something went wrong. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-page">
      <div className="upload-container" style={{ maxWidth: 440, textAlign: 'center' }}>
        <h2>Welcome back</h2>
        <p className="subtitle">Sign in to your Orderly account</p>

        <form onSubmit={handleSubmit} className="preferences-form">
          <div className="form-group">
            <label className="form-label">Email</label>
            <input
              type="email"
              className="form-select"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => { setEmail(e.target.value); setErrors(prev => ({ ...prev, email: '' })); }}
            />
            {errors.email && <div className="message error">{errors.email}</div>}
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-select"
              placeholder="Your password"
              value={password}
              onChange={(e) => { setPassword(e.target.value); setErrors(prev => ({ ...prev, password: '' })); }}
            />
            {errors.password && <div className="message error">{errors.password}</div>}
          </div>

          {errors.server && <div className="message error">{errors.server}</div>}

          <div className="form-actions">
            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </div>
        </form>

        <p style={{ textAlign: 'center', marginTop: 20, fontSize: 14, color: '#666' }}>
          Don't have an account?{' '}
          <Link to="/register" style={{ color: '#4a9d6f', fontWeight: 600 }}>
            Create account
          </Link>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
