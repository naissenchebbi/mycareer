import React from 'react';
import './FeedItem.css';

const typeConfig = {
  news: { label: 'Actualité', tone: 'news' },
  paper: { label: 'Papier', tone: 'paper' },
  job: { label: 'Offre', tone: 'job' },
};

const FeedItem = ({ item }) => {
  const config = typeConfig[item.type] || typeConfig.news;

  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    if (Number.isNaN(date.getTime())) return '';
    return date.toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    });
  };

  const dateLabel = formatDate(item.published);
  const authors = item.authors || [];

  return (
    <article className={`feed-item tone-${config.tone}`}>
      <div className="feed-item-header">
        <span className="feed-item-type">{config.label}</span>
        {dateLabel && <time className="feed-item-date">{dateLabel}</time>}
      </div>

      <h3 className="feed-item-title">{item.title}</h3>

      {item.company && (
        <p className="feed-item-meta">
          {item.company}
          {item.location ? ` · ${item.location}` : ''}
        </p>
      )}

      {authors.length > 0 && (
        <p className="feed-item-meta">
          {authors.slice(0, 3).join(', ')}
          {authors.length > 3 ? ' et al.' : ''}
        </p>
      )}

      {item.source && (
        <a
          href={item.source}
          target="_blank"
          rel="noopener noreferrer"
          className="feed-item-link"
        >
          Ouvrir la source
        </a>
      )}
    </article>
  );
};

export default FeedItem;
