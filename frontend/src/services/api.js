import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  timeout: 60000,
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Erreur API:', error.message);
    return Promise.reject(error);
  }
);

export const sendMessage = async (message, userId, domain, sessionId = null) => {
  const response = await api.post('/api/chat', {
    message,
    user_id: userId,
    domain,
    session_id: sessionId,
  });
  return response.data;
};

export const getDigest = async (userId, domain = 'AI') => {
  const response = await api.get(`/api/digest/${userId}`, { params: { domain } });
  return response.data;
};

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;