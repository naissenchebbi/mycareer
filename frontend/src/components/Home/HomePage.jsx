import React from 'react';
import './HomePage.css';

const HomePage = ({ onNavigate, domain = 'AI' }) => {
  const features = [
    {
      icon: '📰',
      title: 'Veille automatique',
      description: 'Actualités, papiers de recherche et offres d\'emploi agrégés pour votre domaine.',
    },
    {
      icon: '🤖',
      title: 'Assistant sourcé',
      description: 'Posez une question et obtenez une réponse appuyée sur des sources vérifiables.',
    },
    {
      icon: '🎯',
      title: 'Fil personnalisé',
      description: 'Le domaine choisi dans les préférences alimente le fil et l\'assistant.',
    },
    {
      icon: '📚',
      title: 'Traçabilité',
      description: 'Chaque réponse cite ses documents. Vous voyez d\'où vient l\'information.',
    },
  ];

  const steps = [
    { num: '01', title: 'Choisissez votre domaine', desc: 'IA, data, web, DevOps ou cybersécurité.' },
    { num: '02', title: 'Parcourez le fil', desc: 'News, papiers et offres, filtrables en un clic.' },
    { num: '03', title: 'Interrogez l\'assistant', desc: 'Des réponses courtes, avec les sources à côté.' },
  ];

  const preview = [
    { tag: 'Papier', title: 'Retrieval-Augmented Generation for Knowledge-Intensive NLP', meta: 'arXiv · cs.CL' },
    { tag: 'Actu', title: 'Les agents outillés arrivent dans les équipes produit', meta: 'Veille du jour' },
    { tag: 'Offre', title: 'ML Engineer — recherche appliquée', meta: 'Remote · IA' },
  ];

  return (
    <div className="home-page">
      <section className="hero">
        <div className="hero-content">
          <p className="eyebrow">Veille · {domain}</p>
          <h1 className="hero-title">
            Votre carrière, tenue à jour par l'IA
          </h1>
          <p className="hero-subtitle">
            MyCareer rassemble l'actualité, les papiers et les offres de votre domaine,
            puis vous laisse interroger cette veille avec des sources citées.
          </p>
          <div className="hero-actions">
            <button className="btn btn-primary" onClick={() => onNavigate('feed')} type="button">
              Explorer le fil
            </button>
            <button className="btn btn-secondary" onClick={() => onNavigate('chat')} type="button">
              Essayer l'assistant
            </button>
          </div>
        </div>

        <aside className="hero-panel" aria-hidden="true">
          <div className="panel-top">
            <span className="live-dot" />
            Fil du jour
          </div>
          {preview.map((item) => (
            <div className="preview-row" key={item.title}>
              <span className="preview-tag">{item.tag}</span>
              <div>
                <strong>{item.title}</strong>
                <small>{item.meta}</small>
              </div>
            </div>
          ))}
        </aside>
      </section>

      <section className="trust">
        <div>
          <strong>3 sources</strong>
          <span>Actualités, recherche, emploi</span>
        </div>
        <div>
          <strong>Réponses citées</strong>
          <span>Chaque affirmation reste traçable</span>
        </div>
        <div>
          <strong>Un domaine</strong>
          <span>Le fil suit vos préférences</span>
        </div>
      </section>

      <section className="features">
        <h2 className="section-title">Pourquoi MyCareer</h2>
        <div className="features-grid">
          {features.map((feature) => (
            <article key={feature.title} className="feature-card">
              <div className="feature-icon" aria-hidden="true">{feature.icon}</div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="steps">
        <h2 className="section-title">Comment ça marche</h2>
        <div className="steps-grid">
          {steps.map((step) => (
            <article key={step.num} className="step-card">
              <div className="step-number">{step.num}</div>
              <h3>{step.title}</h3>
              <p>{step.desc}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="cta">
        <div>
          <h2>Commencez par le fil du jour</h2>
          <p>Le domaine actif est <strong>{domain}</strong>. Vous pouvez le changer dans les préférences.</p>
        </div>
        <button className="btn btn-light" onClick={() => onNavigate('feed')} type="button">
          Ouvrir le fil
        </button>
      </section>
    </div>
  );
};

export default HomePage;
