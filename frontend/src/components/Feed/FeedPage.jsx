import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { getDigest } from '../../services/api';
import FeedItem from './FeedItem';
import './FeedPage.css';

const FeedPage = ({ domain = 'AI', sources, onNavigate }) => {
  const [digest, setDigest] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');
  const [query, setQuery] = useState('');

  const enabled = sources || { news: true, papers: true, jobs: true };

  const loadFeed = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getDigest('user123', domain);
      setDigest(data);
    } catch (err) {
      setError("Impossible de charger le fil d'actualité. Vérifiez que le backend est lancé.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [domain]);

  useEffect(() => {
    loadFeed();
  }, [loadFeed]);

  const items = useMemo(() => {
    if (!digest) return [];

    const news = enabled.news ? (digest.news || []).map((n) => ({ ...n, type: 'news' })) : [];
    const papers = enabled.papers ? (digest.papers || []).map((p) => ({ ...p, type: 'paper' })) : [];
    const jobs = enabled.jobs ? (digest.jobs || []).map((j) => ({ ...j, type: 'job' })) : [];

    let list = [...news, ...papers, ...jobs];
    if (filter === 'news') list = news;
    if (filter === 'papers') list = papers;
    if (filter === 'jobs') list = jobs;

    const needle = query.trim().toLowerCase();
    if (!needle) return list;

    return list.filter((item) => {
      const haystack = [
        item.title,
        item.company,
        item.location,
        ...(item.authors || []),
      ]
        .filter(Boolean)
        .join(' ')
        .toLowerCase();
      return haystack.includes(needle);
    });
  }, [digest, enabled.news, enabled.papers, enabled.jobs, filter, query]);

  const counts = {
    all: (enabled.news ? digest?.news?.length || 0 : 0)
      + (enabled.papers ? digest?.papers?.length || 0 : 0)
      + (enabled.jobs ? digest?.jobs?.length || 0 : 0),
    news: enabled.news ? digest?.news?.length || 0 : 0,
    papers: enabled.papers ? digest?.papers?.length || 0 : 0,
    jobs: enabled.jobs ? digest?.jobs?.length || 0 : 0,
  };

  const filters = [
    { id: 'all', label: 'Tout', count: counts.all },
    { id: 'news', label: 'Actualités', count: counts.news },
    { id: 'papers', label: 'Papiers', count: counts.papers },
    { id: 'jobs', label: 'Offres', count: counts.jobs },
  ];

  return (
    <div className="feed-page">
      <header className="feed-header">
        <div>
          <p className="feed-kicker">Veille personnalisée</p>
          <h1>Fil d'actualité</h1>
          <p className="feed-subtitle">
            {digest?.summary || 'News, papiers et offres pour votre domaine.'}
          </p>
        </div>
        <div className="feed-header-actions">
          <button className="domain-chip" type="button" onClick={() => onNavigate?.('preferences')}>
            Domaine · {domain}
          </button>
          <button className="refresh-btn" type="button" onClick={loadFeed} disabled={loading}>
            {loading ? 'Chargement…' : 'Actualiser'}
          </button>
        </div>
      </header>

      <div className="feed-toolbar">
        <div className="feed-filters" role="tablist" aria-label="Filtrer le fil">
          {filters.map((f) => (
            <button
              key={f.id}
              type="button"
              role="tab"
              aria-selected={filter === f.id}
              className={`filter-btn ${filter === f.id ? 'active' : ''}`}
              onClick={() => setFilter(f.id)}
            >
              {f.label}
              <span className="filter-count">{f.count}</span>
            </button>
          ))}
        </div>
        <label className="feed-search">
          <span className="sr-only">Rechercher</span>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Rechercher un titre, un auteur, une entreprise…"
          />
        </label>
      </div>

      {loading && (
        <div className="feed-list" aria-busy="true" aria-label="Chargement du fil">
          {[0, 1, 2].map((n) => (
            <div className="skeleton-card" key={n}>
              <div className="skeleton sk-pill" />
              <div className="skeleton sk-line" />
              <div className="skeleton sk-line short" />
            </div>
          ))}
        </div>
      )}

      {!loading && error && (
        <div className="feed-error">
          <p>{error}</p>
          <button onClick={loadFeed} className="retry-btn" type="button">Réessayer</button>
        </div>
      )}

      {!loading && !error && (
        <div className="feed-list">
          {items.length === 0 ? (
            <div className="feed-empty">
              <h2>Rien à afficher</h2>
              <p>
                {query
                  ? 'Aucun résultat pour cette recherche.'
                  : 'Activez au moins une source dans les préférences, ou changez de filtre.'}
              </p>
            </div>
          ) : (
            items.map((item, idx) => (
              <FeedItem key={`${item.type}-${item.title}-${idx}`} item={item} />
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default FeedPage;
