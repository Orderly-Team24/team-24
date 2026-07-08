import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';import Header from './components/common/Header';
import Footer from './components/common/Footer';
import UploadMenu from './pages/UploadMenu';
import FoodRecommenderPage from './pages/FoodRecommenderPage';
import Questionnaire from './pages/Questionnaire';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import './styles/App.css';

function ProtectedRoute({ children }) {
  const token = localStorage.getItem('orderly_access_token');
  if (!token) return <Navigate to="/login" />;
  return children;
}

function PublicRoute({ children }) {
  const token = localStorage.getItem('orderly_access_token');
  if (token) return <Navigate to="/upload" />;
  return children;
}

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/login" element={<PublicRoute><LoginPage /></PublicRoute>} />
            <Route path="/register" element={<PublicRoute><RegisterPage /></PublicRoute>} />
            <Route path="/" element={<ProtectedRoute><UploadMenu /></ProtectedRoute>} />
            <Route path="/questionnaire" element={<ProtectedRoute><Questionnaire /></ProtectedRoute>} />
            <Route path="/upload" element={<ProtectedRoute><UploadMenu /></ProtectedRoute>} />
            <Route path="/food-recommender" element={<ProtectedRoute><FoodRecommenderPage /></ProtectedRoute>} />
            <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
