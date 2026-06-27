import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

const API_BASE_URL = 'https://team-24-1.onrender.com';

const FoodRecommenderPage = () => {
  const navigate = useNavigate();
  const [dish, setDish] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [noMoreOptions, setNoMoreOptions] = useState(false);

  useEffect(() => {
    const storedSessionId = localStorage.getItem('sessionId');
    
    if (!storedSessionId) {
      setError('Please upload a menu first to get recommendations.');
      setLoading(false);
      return;
    }
    
    setSessionId(storedSessionId);
    
    const loadData = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/display/recommendation`, {
          method: 'GET',
          headers: {'Content-Type': 'application/json', 'session-id': storedSessionId,
          },
        });

        if (!response.ok) {
          throw new Error('Failed to load recommendations');
        }

        const data = await response.json();
        setDish(data.dish || data);
        setError(null);
        setNoMoreOptions(false);
      } catch (err) {
        setError('Failed to load recommendations');
        console.error('Error loading recommendations:', err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const handleOrder = () => {
    alert(`"${dish.name}" Saved! Bon appétit`);
    console.log('Ordered:', dish.name);
  };

  const handleAnotherOption = async () => {
    if (loading || noMoreOptions) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/display/another-option`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'session-id': sessionId,
        },
        body: JSON.stringify({ 
          sessionId: sessionId,
          currentDishId: dish?.id
        }),
      });

      if (response.status === 404) {
        setNoMoreOptions(true);
        setError('No more options available');
        setLoading(false);
        return;
      }

      if (!response.ok) {
        let errorMsg = 'Failed to get another option';
        try {
          const errData = await response.json();
          errorMsg = errData.error || errorMsg;
        } catch {}
        throw new Error(errorMsg);
      }

      const data = await response.json();
      setDish(data.dish || data);
      setError(null);
      setNoMoreOptions(false);
      
    } catch (err) {
      setError(err.message || 'Failed to load another option');
      console.error('Error getting another option:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleEndSession = () => {
    localStorage.removeItem('sessionId');
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
        <button 
          className="btn-primary" 
          onClick={() => navigate('/')}
        >
          Go to Home
        </button>
      </div>
    );
  }

  if (!dish) {
    return (
      <div className="center">
        <p>No dishes found</p>
        <button 
          className="btn-secondary" 
          onClick={() => navigate('/')}
          style={{ marginTop: '20px' }}
        >
          Go to Home
        </button>
      </div>
    );
  }

  return (
    <div>
      <main className="main">
        <div className="container">
          <h2 className="title">Top pick for you</h2>
          <p className="subtitle">
            Personal recommendation based on your preferences
          </p>

          <div className="card-wrapper">
            <div className="card">
              <div className="card-content">
                <h3>{dish.name}</h3>
                <div className="price">${dish.price}</div>
                <div className="desc">{dish.description}</div>
                <div className="ingredients">{dish.ingredients?.join(' • ') || ''}</div>
                <div className="reason">{dish.reason || 'Recommended for you'}</div>

                {error && (
                  <div className="error-message" style={{ color: '#e53e3e', margin: '10px 0' }}>
                    {error}
                  </div>
                )}

                <div className="actions">
                  <button 
                    className="btn-primary" 
                    onClick={handleOrder}
                    disabled={loading}
                  >
                    I'll order it
                  </button>
                  
                  <button 
                    className="btn-secondary" 
                    onClick={handleAnotherOption}
                    disabled={loading || noMoreOptions}
                  >
                    {loading ? 'Loading...' : 
                     noMoreOptions ? 'No more options' : 
                     'Another option'}
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
