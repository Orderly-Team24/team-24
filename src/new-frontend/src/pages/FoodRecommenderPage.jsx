import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

const API_RECOMMENDER = 'https://team-24.onrender.com';

const FoodRecommenderPage = () => {
  const navigate = useNavigate();
  const [dish, setDish] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saved, setSaved] = useState(false);
  const callCounter = useRef(0);

  useEffect(() => {
    loadRecommendation();
  }, []);

  const loadRecommendation = async () => {
    setLoading(true);
    setError(null);
    setSaved(false);

    const menu = JSON.parse(localStorage.getItem('orderly_menu') || 'null');

    try {
      const response = await fetch(`${API_RECOMMENDER}/display/recommendations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: callCounter.current > 0 ? `option ${callCounter.current}` : 'Recommend a dish',
          menu: menu || [],
        }),
      });

      if (!response.ok) {
        let detail = `HTTP ${response.status}`;
        try {
          const body = await response.json();
          if (body && body.detail) detail = body.detail;
        } catch (_) {}
        throw new Error(detail);
      }

      const data = await response.json();

      if (!data.recommendations || data.recommendations.length === 0) {
        setDish(null);
        setError('No recommendations found.');
      } else {
        setDish(data.recommendations[0]);
      }
    } catch (err) {
      setError(err.message || 'Failed to load recommendations');
      console.error('Error loading recommendations:', err);
    } finally {
      setLoading(false);
      setSaved(false);
    }
  };

  const handleOrder = async () => {
    if (!dish || saved) return;

    try {
      const response = await fetch(`${API_RECOMMENDER}/history/orders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Id': 'user_123',
        },
        body: JSON.stringify(dish),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      setSaved(true);
    } catch (err) {
      console.error('Save order failed:', err);
      setError('Could not save order: ' + (err.message || String(err)));
    }
  };

  const handleAnotherOption = () => {
    callCounter.current += 1;
    loadRecommendation();
  };

  const handleEndSession = () => {
    localStorage.removeItem('orderly_menu');
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
        <h3 style={{ color: '#e53e3e' }}>{error}</h3>
        <button className="btn-primary" onClick={() => navigate('/upload')} style={{ marginTop: '20px' }}>
          Upload a menu
        </button>
      </div>
    );
  }

  return (
    <div>
      <main className="main">
        <div className="container">
          <h2 className="title">Top pick for you</h2>
          <p className="subtitle">Personal recommendation based on your menu</p>

          <div className="card-wrapper">
            <div className="card">
              <div className="card-content">
                <h3>{dish.name}</h3>
                <div className="price">${dish.price}</div>
                <div className="desc">{dish.description}</div>
                <div className="ingredients">{dish.ingredients?.join(' • ') || ''}</div>
                <div className="reason">{dish.reason || 'Recommended for you'}</div>

                {error && (
                  <div style={{ color: '#e53e3e', margin: '10px 0', fontSize: '14px' }}>
                    {error}
                  </div>
                )}

                <div className="actions">
                  <button
                    className={saved ? 'btn-saved' : 'btn-primary'}
                    onClick={handleOrder}
                    disabled={saved}
                  >
                    {saved ? 'Saved ✓' : "I'll order it"}
                  </button>

                  <button
                    className="btn-secondary"
                    onClick={handleAnotherOption}
                    disabled={loading}
                  >
                    Another option
                  </button>

                  <button
                    className="btn-tertiary"
                    onClick={handleEndSession}
                    disabled={loading}
                  >
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
