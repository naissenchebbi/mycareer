import React, { useEffect, useState } from 'react';
import './PreferencesPage.css';

const domains = [
  { value: 'AI', label: 'Intelligence artificielle', hint: 'LLM, RAG, agents' },
  { value: 'Data Science', label: 'Data science', hint: 'Stats, ML, visualisation' },
  { value: 'Web Dev', label: 'Développement web', hint: 'Frontend, API, produit' },
  { value: 'DevOps', label: 'DevOps', hint: 'Cloud, CI, infra' },
  { value: 'Cybersecurity', label: 'Cybersécurité', hint: 'AppSec, SOC, cloud' },
];

const PreferencesPage = ({ preferences, onSave }) => {
  const [draft, setDraft] = useState(preferences);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    setDraft(preferences);
  }, [preferences]);

  const handleChange = (field, value) => {
    setDraft((prev) => ({ ...prev, [field]: value }));
    setSaved(false);
  };

  const handleSourceChange = (source) => {
    setDraft((prev) => ({
      ...prev,
      sources: { ...prev.sources, [source]: !prev.sources[source] },
    }));
    setSaved(false);
  };

  const keywords = draft.keywords
    .split(',')
    .map((word) => word.trim())
    .filter(Boolean);

  const removeKeyword = (word) => {
    handleChange(
      'keywords',
      keywords.filter((item) => item !== word).join(', ')
    );
  };

  const handleSave = () => {
    onSave(draft);
    setSaved(true);
  };

  return (
    <div className="preferences-page">
      <header className="preferences-header">
        <p className="feed-kicker">Réglages</p>
        <h1>Préférences</h1>
        <p className="preferences-subtitle">
          Le domaine choisi s'applique au fil d'actualité et à l'assistant.
        </p>
      </header>

      <form
        className="preferences-form"
        onSubmit={(e) => {
          e.preventDefault();
          handleSave();
        }}
      >
        <fieldset className="form-group">
          <legend className="form-label">Domaine d'intérêt</legend>
          <div className="domain-grid">
            {domains.map((item) => (
              <label
                key={item.value}
                className={`domain-card ${draft.domain === item.value ? 'selected' : ''}`}
              >
                <input
                  type="radio"
                  name="domain"
                  value={item.value}
                  checked={draft.domain === item.value}
                  onChange={() => handleChange('domain', item.value)}
                />
                <strong>{item.label}</strong>
                <span>{item.hint}</span>
              </label>
            ))}
          </div>
        </fieldset>

        <div className="form-group">
          <label className="form-label" htmlFor="keywords">Mots-clés</label>
          <input
            id="keywords"
            type="text"
            value={draft.keywords}
            onChange={(e) => handleChange('keywords', e.target.value)}
            placeholder="Ex. RAG, LLM, Machine Learning"
            className="form-input"
          />
          <small className="form-hint">Séparez les termes par des virgules. Cliquez un mot pour le retirer.</small>
          {keywords.length > 0 && (
            <div className="keyword-list">
              {keywords.map((word) => (
                <button
                  key={word}
                  type="button"
                  className="keyword-chip"
                  onClick={() => removeKeyword(word)}
                >
                  {word}
                  <span aria-hidden="true">×</span>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="email">Email du digest</label>
          <input
            id="email"
            type="email"
            value={draft.email}
            onChange={(e) => handleChange('email', e.target.value)}
            placeholder="vous@email.com"
            className="form-input"
          />
        </div>

        <fieldset className="form-group">
          <legend className="form-label">Fréquence du digest</legend>
          <div className="segmented">
            {[
              { value: 'daily', label: 'Quotidien' },
              { value: 'weekly', label: 'Hebdomadaire' },
              { value: 'never', label: 'Jamais' },
            ].map((item) => (
              <label key={item.value}>
                <input
                  type="radio"
                  name="frequency"
                  value={item.value}
                  checked={draft.frequency === item.value}
                  onChange={() => handleChange('frequency', item.value)}
                />
                {item.label}
              </label>
            ))}
          </div>
        </fieldset>

        <fieldset className="form-group">
          <legend className="form-label">Sources du fil</legend>
          <div className="source-list">
            {[
              { key: 'news', label: 'Actualités', hint: 'Articles et annonces' },
              { key: 'papers', label: 'Papiers de recherche', hint: 'Prépublications et articles' },
              { key: 'jobs', label: "Offres d'emploi", hint: 'Postes liés au domaine' },
            ].map((source) => (
              <label key={source.key} className="source-row">
                <span>
                  <strong>{source.label}</strong>
                  <small>{source.hint}</small>
                </span>
                <input
                  type="checkbox"
                  checked={draft.sources[source.key]}
                  onChange={() => handleSourceChange(source.key)}
                />
              </label>
            ))}
          </div>
        </fieldset>

        <div className="form-actions">
          <button className="btn-save" type="submit">Enregistrer</button>
          {saved && <span className="save-success">Préférences enregistrées</span>}
        </div>
      </form>
    </div>
  );
};

export default PreferencesPage;
