import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

function Questionnaire() {
  const navigate = useNavigate();
  const [likes, setLikes] = useState('');
  const [dislikes, setDislikes] = useState('');
  const [allergies, setAllergies] = useState('');
  const [error, setError] = useState('');

  const parseList = (value) =>
    value.split(',').map(item => item.trim()).filter(Boolean);

  const handleSubmit = (e) => {
    e.preventDefault();
    localStorage.setItem('orderly_preferences', JSON.stringify({
      cuisine: null,
      likes: parseList(likes),
      dislikes: parseList(dislikes),
      allergies: parseList(allergies),
    }));
    navigate('/upload');
  };

  const handleReset = () => {
    setLikes('');
    setDislikes('');
    setAllergies('');
    setError('');
  };

  return (
    <div className="upload-page">
      <div className="upload-container" style={{ maxWidth: 600 }}>
        <h2>Your Food Preferences</h2>
        <p className="subtitle">Step 1 of 3 — Tell us your taste so we can find the perfect dish</p>

        <form onSubmit={handleSubmit} className="preferences-form">
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

          {error && <div className="message error">{error}</div>}

          <div className="form-actions">
            <button type="submit" className="submit-btn">Next: Upload Menu →</button>
            <button type="button" className="remove-btn" onClick={handleReset}>Reset</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Questionnaire;
