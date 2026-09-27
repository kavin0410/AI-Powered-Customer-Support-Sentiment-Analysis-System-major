/**
 * Centralized API service using Axios for communicating with the FastAPI backend.
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Interceptor for uniform error extraction
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    let message = 'An unexpected network error occurred.';
    if (error.response) {
      // Backend returned an error response
      message = error.response.data?.detail || `Server error (${error.response.status})`;
    } else if (error.request) {
      // Backend didn't respond
      message = 'Unable to connect to the backend server. Please verify FastAPI is running on port 8000.';
    }
    return Promise.reject(new Error(message));
  }
);

export const checkHealth = () => apiClient.get('/health');

export const getDashboard = () => apiClient.get('/dashboard');

export const predictFeedback = (text) => apiClient.post('/predict', { text });

export const getFeedback = (params = {}) => apiClient.get('/feedback', { params });

export const getFeedbackById = (id) => apiClient.get(`/feedback/${id}`);

export const getSentimentAnalytics = () => apiClient.get('/analytics/sentiment');

export const getIssueAnalytics = () => apiClient.get('/analytics/issues');

export const getBusinessInsights = () => apiClient.get('/insights');

export default {
  checkHealth,
  getDashboard,
  predictFeedback,
  getFeedback,
  getFeedbackById,
  getSentimentAnalytics,
  getIssueAnalytics,
  getBusinessInsights,
};
