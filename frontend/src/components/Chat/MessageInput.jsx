import React, { useState } from 'react';

const suggestions = [
  'Liste les papiers sur le RAG',
  "Qu'est-ce que le RAG ?",
  'Comment fonctionne ChromaDB ?',
  'Parle-moi de Groq',
];

const MessageInput = ({ onSend, isLoading, showSuggestions = true }) => {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim() && !isLoading) {
      onSend(text);
      setText('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="message-input-container">
      {showSuggestions && (
        <div className="suggestions">
          {suggestions.map((suggestion) => (
            <button
              key={suggestion}
              className="suggestion-btn"
              type="button"
              onClick={() => onSend(suggestion)}
              disabled={isLoading}
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}

      <form onSubmit={handleSubmit} className="input-form">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Posez votre question…"
          disabled={isLoading}
          rows={1}
          aria-label="Votre question"
        />
        <button type="submit" disabled={isLoading || !text.trim()}>
          {isLoading ? '…' : 'Envoyer'}
        </button>
      </form>
    </div>
  );
};

export default MessageInput;
