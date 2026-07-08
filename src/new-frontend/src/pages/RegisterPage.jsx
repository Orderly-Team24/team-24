import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../styles/App.css';

const API_URL = 'https://team-24.onrender.com';

function RegisterPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const validate = () => {
    const newErrors = {};
    if (!email) {
      newErrors.email = 'Email is required.';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'Please enter a valid email address.';
    }
    if (!username) {
      newErrors.username = 'Username is required.';
    }
    if (!password) {
      newErrors.password = 'Password is required.';
    }
    if (!confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password.';
    } else if (password !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match.';
    }
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (loading) return;
    const newErrors = validate();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    setErrors({});
    setLoading(true);

    try {
      const registerResponse = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email,
          username,
          password,
          preferences: {},
        }),
      });

      if (!registerResponse.ok) {
        const body = await registerResponse.json().catch(() => ({}));
        setErrors({ server: body.detail || 'Could not create your account. Please try again.' });
        return;
      }

      // /auth/register doesn't issue tokens itself, so log in right away to
      // get one — Questionnaire.jsx needs it to save preferences to this
      // account instead of just localStorage.
      const loginResponse = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (loginResponse.ok) {
        const tokens = await loginResponse.json();
        localStorage.setItem('orderly_access_token', tokens.access_token);
        localStorage.setItem('orderly_refresh_token', tokens.refresh_token);
      }

      navigate('/questionnaire');
    } catch (err) {
      setErrors({ server: 'Something went wrong. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  const clearError = (field) => setErrors(prev => ({ ...prev, [field]: '' }));

  return (
    <div className="upload-page">
      <div className="upload-container" style={{ maxWidth: 440, textAlign: 'center' }}>
        <h2>Create account</h2>
        <p className="subtitle">Join Orderly to get personalized recommendations</p>

        <form onSubmit={handleSubmit} className="preferences-form">
          <div className="form-group">
            <label className="form-label">Email</label>
            <input
              type="email"
              className="form-select"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => { setEmail(e.target.value); clearError('email'); }}
            />
            {errors.email && <div className="message error">{errors.email}</div>}
          </div>

          <div className="form-group">
            <label className="form-label">Username</label>
            <input
              type="text"
              className="form-select"
              placeholder="Your username"
              value={username}
              onChange={(e) => { setUsername(e.target.value); clearError('username'); }}
            />
            {errors.username && <div className="message error">{errors.username}</div>}
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-select"
              placeholder="Your password"
              value={password}
              onChange={(e) => { setPassword(e.target.value); clearError('password'); }}
            />
            {errors.password && <div className="message error">{errors.password}</div>}
          </div>

          <div className="form-group">
            <label className="form-label">Confirm Password</label>
            <input
              type="password"
              className="form-select"
              placeholder="Repeat your password"
              value={confirmPassword}
              onChange={(e) => { setConfirmPassword(e.target.value); clearError('confirmPassword'); }}
            />
            {errors.confirmPassword && <div className="message error">{errors.confirmPassword}</div>}
          </div>

          {errors.server && <div className="message error">{errors.server}</div>}

          <div className="form-actions">
            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? 'Creating account...' : 'Next: Set preferences →'}
            </button>
          </div>
        </form>

        <p style={{ textAlign: 'center', marginTop: 20, fontSize: 14, color: '#666' }}>
          Already have an account?{' '}
          <Link to="/login" style={{  color: '#4a9d6f', fontWeight: 600 }}>
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
