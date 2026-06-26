import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

const dishesData = [
  {
    id: 1,
    name: 'Chicken Noodle Soup',
    price: 15.99,
    description: 'Hearty soup with chicken and fresh herbs',
    ingredients: ['Chicken', 'Noodles', 'Carrots', 'Onion'],
    reason: 'Matches your budget • No allergens'
  },
  {
    id: 2,
    name: 'Greek Salad with Feta',
    price: 12.50,
    description: 'Fresh Mediterranean salad with olives and feta',
    ingredients: ['Tomatoes', 'Cucumber', 'Feta', 'Olives'],
    reason: 'Within your budget • Vegetarian'
  },
  {
    id: 3,
    name: 'Grilled Salmon with Vegetables',
    price: 24.00,
    description: 'Perfectly grilled salmon with seasonal vegetables',
    ingredients: ['Salmon', 'Zucchini', 'Lemon', 'Rosemary'],
    reason: 'Chef\'s recommendation • Popular dish'
  }
];

const FoodRecommenderPage = () => {
  const navigate = useNavigate();
  const [dish, setDish] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        await new Promise(resolve => setTimeout(resolve, 800));
        setDish(dishesData[0]);
        setError(null);
      } catch (err) {
        setError('Failed to load recommendations');
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
    setLoading(true);
    try {
      await new Promise(resolve => setTimeout(resolve, 800));
      const randomIndex = Math.floor(Math.random() * dishesData.length);
      setDish(dishesData[randomIndex]);
      setError(null);
    } catch (err) {
      setError('Failed to load recommendations');
    } finally {
      setLoading(false);
    }
  };

  const handleEndSession = () => {
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

  if (error) {
    return (
      <div className="center">
        <h3 style={{ color: '#e53e3e' }}>{error}</h3>
        <p>Please try again later.</p>
      </div>
    );
  }

  if (!dish) {
    return (
      <div className="center">
        <p>No dishes found</p>
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
                <div className="ingredients">{dish.ingredients.join(' • ')}</div>
                <div className="reason">{dish.reason}</div>

                <div className="actions">
                  <button className="btn-primary" onClick={handleOrder}>
                    I'll order it
                  </button>
                  <button className="btn-secondary" onClick={handleAnotherOption}>
                    Another option
                  </button>
                  <button className="btn-tertiary" onClick={handleEndSession}>
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