import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="header">
      <div className="logo">
        <Link to="/">Orderly</Link>
      </div>
      
      <nav className="navigation">
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/profile">Profile</Link></li>
          <Link to="/history">History</Link>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
