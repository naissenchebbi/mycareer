import React from 'react';

function renderText(text) {
  return String(text)
    .split(/(\*\*[^*]+\*\*)/g)
    .map((part, index) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={index}>{part.slice(2, -2)}</strong>;
      }
      return <span key={index}>{part}</span>;
    });
}

const MessageList = ({ messages }) => {
  return (
    <div className="message-list">
      {messages.map((msg) => (
        <div
          key={msg.id}
          className={`message ${msg.sender === 'user' ? 'user-message' : 'bot-message'}`}
        >
          <div className="message-avatar" aria-hidden="true">
            {msg.sender === 'user' ? 'Vous' : 'AI'}
          </div>
          <div className="message-content">
            <div className="message-text">{renderText(msg.text)}</div>
            {msg.sources && msg.sources.length > 0 && (
              <div className="message-sources">
                <small>Sources</small>
                {msg.sources.map((source, idx) => (
                  <div key={idx} className="source-item">
                    <span className="source-title">
                      [{source.id}] {source.title}
                    </span>
                    {source.source && (
                      <a
                        href={source.source}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="source-link"
                      >
                        Ouvrir
                      </a>
                    )}
                  </div>
                ))}
              </div>
            )}
            <div className="message-time">
              {new Date(msg.timestamp).toLocaleTimeString('fr-FR', {
                hour: '2-digit',
                minute: '2-digit',
              })}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MessageList;
