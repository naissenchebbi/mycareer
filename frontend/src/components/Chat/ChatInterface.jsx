import React, { useEffect, useRef, useState } from 'react';
import { sendMessage } from '../../services/api';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import './ChatInterface.css';

const welcomeText = (domain) =>
  `Bonjour. Je suis l'assistant MyCareer pour le domaine ${domain}.\n\nPosez une question sur les papiers, le RAG ou les LLM. Les réponses citent leurs sources.`;

const ChatInterface = ({ userId = 'user123', domain = 'AI' }) => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    setSessionId(null);
    setMessages([
      {
        id: 'welcome',
        sender: 'bot',
        text: welcomeText(domain),
        timestamp: new Date(),
      },
    ]);
  }, [domain]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const resetConversation = () => {
    setSessionId(null);
    setMessages([
      {
        id: `welcome-${Date.now()}`,
        sender: 'bot',
        text: welcomeText(domain),
        timestamp: new Date(),
      },
    ]);
  };

  const handleSendMessage = async (text) => {
    if (!text.trim() || isLoading) return;

    const userMessage = {
      id: Date.now().toString(),
      sender: 'user',
      text,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await sendMessage(text, userId, domain, sessionId);
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: 'bot',
          text: response.reply,
          sources: response.sources || [],
          timestamp: new Date(),
        },
      ]);
      if (response.session_id) setSessionId(response.session_id);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: 'bot',
          text: 'Une erreur est survenue. Vérifiez que le backend est bien lancé.',
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-shell">
      <div className="chat-container">
        <div className="chat-header">
          <div>
            <p className="chat-kicker">Assistant</p>
            <h2>MyCareer</h2>
          </div>
          <div className="chat-header-actions">
            <span className="domain-badge">{domain}</span>
            <button className="reset-btn" type="button" onClick={resetConversation}>
              Nouvelle conversation
            </button>
          </div>
        </div>

        <div className="chat-messages">
          <MessageList messages={messages} />
          {isLoading && (
            <div className="message bot-message" aria-live="polite">
              <div className="message-avatar" aria-hidden="true">AI</div>
              <div className="message-content typing" aria-label="L'assistant écrit">
                <span />
                <span />
                <span />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <MessageInput
          onSend={handleSendMessage}
          isLoading={isLoading}
          showSuggestions={messages.length <= 1}
        />
      </div>
    </div>
  );
};

export default ChatInterface;
