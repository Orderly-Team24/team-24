import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

const API_RECOMMENDER = 'https://team-24.onrender.com';

function buildPreferences() {
  const raw = JSON.parse(localStorage.getItem('orderly_preferences') || 'null');
  const budget = localStorage.getItem('orderly_budget');
  if (!raw && !budget) return null;
  return {exclude_ingredients: [
      ...(raw?.allergies || []),
      ...(raw?.dislikes || []),
    ],
    favorite_ingredients: raw?.likes || [],
    max_budget: budget ? parseFloat(budget) : null,
    restrictions: raw?.restrictions || [],
  };
}

const FoodRecommenderPage = () => {
  const navigate = useNavigate();
  const [dish, setDish] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saved, setSaved] = useState(false);
  const callCounter = useRef(0);

  useEffect(() => { loadRecommendation(); }, []);

  const loadRecommendation = async () => {
    setLoading(true);
    setError(null);
    setSaved(false);

    const menu = JSON.parse(localStorage.getItem('orderly_menu') || 'null');
    const preferences = buildPreferences();
    const mood = sessionStorage.getItem('orderly_mood') || '';

    try {
      const response = await fetch(`${API_RECOMMENDER}/display/recommendations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: callCounter.current > 0
            ? `${mood || 'Recommend a dish'}. (option ${callCounter.current})`
            : (mood || 'Recommend a dish'),
          menu: menu || [],
          preferences,
        }),
      });

      if (!response.ok) {
        let detail = `HTTP ${response.status}`;
        try { const body = await response.json(); if (body?.detail) detail = body.detail; } catch (_) {}
        throw new Error(detail);
      }

      const data = await response.json();
      if (!data.recommendations || data.recommendations.length === 0) {
        setDish(null);
        setError('No dishes found within your budget. Try raising it on the previous step.');
      } else {
        setDish(data.recommendations[0]);
      }
    } catch (err) {
      setError(err.message || 'Failed to load recommendations');
    } finally {
      setLoading(false);
    }
  };

  const handleOrder = async () => {
    if (!dish || saved) return;
    try {
      const response = await fetch(`${API_RECOMMENDER}/history/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-User-Id': 'user_123' },
        body: JSON.stringify(dish),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      setSaved(true);
    } catch (err) {
      setError('Could not save order: ' + (err.message || String(err)));
    }
  };

  const handleAnotherOption = () => {
    callCounter.current += 1;
    loadRecommendation();
  };

  const handleEndSession = () => {
    localStorage.removeItem('orderly_menu');
    localStorage.removeItem('orderly_preferences');
    localStorage.removeItem('orderly_budget');
    sessionStorage.removeItem('orderly_mood');
    navigate('/');
  };

  if (loading) {
    return (
      <div className="center">
        <div className="spinner"></div>
        <p>Finding the best dish for you...</p>
      </div>
    );
  }

  if (error && !dish) {
    return (
      <div className="center">
        <h3 style={{ color: '#e53e3e', marginBottom: 16 }}>{error}</h3>
        <button className="btn-primary" onClick={() => navigate('/upload')} style={{ marginBottom: 12, maxWidth: 260 }}>
          ← Change budget / photo
        </button>
        <button className="btn-secondary" onClick={handleAnotherOption} style={{ maxWidth: 260 }}>
          Try anyway
        </button>
      </div>
    );
  }

  return (
    <div>
      <main className="main">
        <div className="container">
          <h2 className="title">Top pick for you</h2>
          <p className="subtitle" style={{ marginBottom: 8 }}>Step 3 of 3 — Your personalized recommendation</p>

          <div className="card-wrapper">
            <div className="card">
              <div className="card-content">
                <h3>{dish.name}</h3>
                {dish.price != null && <div className="price">${dish.price}</div>}
                <div className="desc">{dish.description}</div>
                <div className="ingredients">{dish.ingredients?.join(' • ') || ''}</div>
                <div className="reason">{dish.reason || 'Recommended for you'}</div>

                {error && (
                  <div style={{ color: '#e53e3e', margin: '10px 0', fontSize: 14 }}>{error}</div>
                )}

                <div className="actions">
                  <button
                    className={saved ? 'btn-saved' : 'btn-primary'}
                    onClick={handleOrder}
                    disabled={saved}
                  >
                    {saved ? 'Saved ✓' : "I'll order it"}
                  </button>
                  <button className="btn-secondary" onClick={handleAnotherOption} disabled={loading}>
                    Another option
                  </button>
                  <button className="btn-tertiary" onClick={handleEndSession} disabled={loading}>
                    End session
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default FoodRecommenderPage;
