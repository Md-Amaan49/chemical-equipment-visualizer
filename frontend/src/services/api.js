import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

// Authentication API calls
export const login = (username, password) => {
  return api.post('/auth/login/', { username, password });
};

export const logout = () => {
  return api.post('/auth/logout/');
};

export const checkAuthStatus = () => {
  return api.get('/auth/user/');
};

// Dataset API calls
export const uploadCSV = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const getAnalytics = (datasetId) => {
  return api.get(`/analytics/${datasetId}/`);
};

export const getDatasets = () => {
  return api.get('/datasets/');
};

export const getHistory = () => {
  return api.get('/history/');
};

export const deleteDataset = (datasetId) => {
  return api.delete(`/datasets/${datasetId}/`);
};

export default api;