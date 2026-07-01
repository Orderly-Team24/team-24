import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import UploadMenu from './pages/UploadMenu';
import FoodRecommenderPage from './pages/FoodRecommenderPage';
import Questionnaire from './pages/Questionnaire';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Questionnaire />} />
            <Route path="/upload" element={<UploadMenu />} />
            <Route path="/food-recommender" element={<FoodRecommenderPage />} /
            <Route path="/login" element={<LoginPage />} />
            <Route path="/food-recommender" element={<FoodRecommenderPage />} />
            <Route path="/register" element={<RegisterPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
