import React, { useState } from 'react';
import './Navbar.css';

const Navbar = ({ currentPage, onNavigate }) => {
  const [open, setOpen] = useState(false);

  const links = [
    { id: 'home', icon: '🏠', label: 'Accueil' },
    { id: 'feed', icon: '📰', label: "Fil d'actualité" },
    { id: 'chat', icon: '💬', label: 'Assistant' },
    { id: 'preferences', icon: '⚙️', label: 'Préférences' },
  ];

  const go = (id) => {
    onNavigate(id);
    setOpen(false);
  };

  return (
    <nav className="navbar">
      <button className="navbar-logo" onClick={() => go('home')} type="button">
        <span className="logo-mark" aria-hidden="true">M</span>
        <span className="logo-text">MyCareer</span>
      </button>

      <button
        className="nav-toggle"
        type="button"
        aria-expanded={open}
        aria-label={open ? 'Fermer le menu' : 'Ouvrir le menu'}
        onClick={() => setOpen((value) => !value)}
      >
        <span />
        <span />
        <span />
      </button>

      <ul className={`navbar-links ${open ? 'open' : ''}`}>
        {links.map((link) => (
          <li key={link.id}>
            <button
              type="button"
              className={`nav-link ${currentPage === link.id ? 'active' : ''}`}
              aria-current={currentPage === link.id ? 'page' : undefined}
              onClick={() => go(link.id)}
            >
              <span aria-hidden="true">{link.icon}</span>
              {link.label}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Navbar;
