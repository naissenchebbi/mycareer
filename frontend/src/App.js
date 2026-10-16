import React, { useEffect, useState } from 'react';
import Navbar from './components/Layout/Navbar';
import HomePage from './components/Home/HomePage';
import FeedPage from './components/Feed/FeedPage';
import ChatInterface from './components/Chat/ChatInterface';
import PreferencesPage from './components/Preferences/PreferencesPage';
import './App.css';

const STORAGE_KEY = 'mycareer_preferences';

const defaultPreferences = {
  domain: 'AI',
  keywords: 'RAG, LLM, AI',
  email: '',
  frequency: 'daily',
  sources: {
    news: true,
    papers: true,
    jobs: true,
  },
};

function loadPreferences() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return defaultPreferences;
    return {
      ...defaultPreferences,
      ...JSON.parse(saved),
      sources: {
        ...defaultPreferences.sources,
        ...(JSON.parse(saved).sources || {}),
      },
    };
  } catch {
    return defaultPreferences;
  }
}

function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [preferences, setPreferences] = useState(defaultPreferences);

  useEffect(() => {
    setPreferences(loadPreferences());
  }, []);

  const savePreferences = (next) => {
    setPreferences(next);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage onNavigate={setCurrentPage} domain={preferences.domain} />;
      case 'feed':
        return (
          <FeedPage
            domain={preferences.domain}
            sources={preferences.sources}
            onNavigate={setCurrentPage}
          />
        );
      case 'chat':
        return <ChatInterface userId="user123" domain={preferences.domain} />;
      case 'preferences':
        return (
          <PreferencesPage preferences={preferences} onSave={savePreferences} />
        );
      default:
        return <HomePage onNavigate={setCurrentPage} domain={preferences.domain} />;
    }
  };

  return (
    <div className="App">
      <Navbar currentPage={currentPage} onNavigate={setCurrentPage} />
      <main className="app-main" key={currentPage}>
        {renderPage()}
      </main>
    </div>
  );
}

export default App;
