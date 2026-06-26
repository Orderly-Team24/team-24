import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div className="home-page">
      <div className="hero-section">
        <h1>Orderly</h1>
        <p>Snap a menu, get top-3 dish recommendations tuned to your taste, budget, and allergies.</p>
      </div>
      
      <div className="features">
        <Link to="/upload" style={{ textDecoration: 'none' }}>
          <div className="feature-card">
            <h3>Get recommendations</h3>
            <p>Send us a photo of the menu and we'll show you recomendations</p>
          </div>
        </Link>
      </div>
    </div>
  );
}

export default HomePage;