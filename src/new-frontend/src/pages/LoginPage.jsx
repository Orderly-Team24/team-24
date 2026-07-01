import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/App.css';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
  };

  return (
    <div className="upload-page">
      <div className="upload-container" style={{ maxWidth: 440, textAlign: 'center' }}>        
        <h2>Welcome!</h2>
        <p className="subtitle">Sign in to your Orderly account</p>

        <form onSubmit={handleSubmit} className="preferences-form">
          <div className="form-group">
            <label className="form-label">Email</label>
            <input
              type="email"
              className="form-select"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-select"
              placeholder="Your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="submit-btn">Sign in</button>
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