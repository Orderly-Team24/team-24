import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import UploadMenu from './pages/UploadMenu';
import HomePage from './pages/HomePage';
import FoodRecommenderPage from './pages/FoodRecommenderPage';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/upload" element={<UploadMenu />} />
            <Route path="/food-recommender" element={<FoodRecommenderPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;