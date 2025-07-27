import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Search API
export const searchCode = async (params: {
  query: string;
  page?: number;
  language?: string;
  complexity?: string;
  quality?: string;
  repositories?: string[];
}) => {
  const response = await api.get('/api/v1/search/', { params });
  return response.data;
};

export const getSearchSuggestions = async (query: string, limit: number = 10) => {
  const response = await api.get('/api/v1/search/suggestions', {
    params: { q: query, limit },
  });
  return response.data;
};

export const findSimilarSnippets = async (snippetId: string, limit: number = 10) => {
  const response = await api.get(`/api/v1/search/similar/${snippetId}`, {
    params: { limit },
  });
  return response.data;
};

export const explainCodeSnippet = async (snippetId: string, context?: string) => {
  const response = await api.post('/api/v1/search/explain', {
    snippet_id: snippetId,
    context,
  });
  return response.data;
};

// Repository API
export const getRepositories = async (params?: {
  page?: number;
  limit?: number;
  status?: string;
}) => {
  const response = await api.get('/api/v1/repositories', { params });
  return response.data;
};

export const indexRepository = async (data: {
  repository_url: string;
  branch?: string;
  include_patterns?: string[];
  exclude_patterns?: string[];
}) => {
  const response = await api.post('/api/v1/index', data);
  return response.data;
};

export const getRepositoryStatus = async (repositoryId: string) => {
  const response = await api.get(`/api/v1/repositories/${repositoryId}/status`);
  return response.data;
};

export const deleteRepository = async (repositoryId: string) => {
  const response = await api.delete(`/api/v1/repositories/${repositoryId}`);
  return response.data;
};

// Analytics API
export const getSearchAnalytics = async (params?: {
  days?: number;
  repository_id?: string;
}) => {
  const response = await api.get('/api/v1/analytics/search', { params });
  return response.data;
};

export const getRepositoryAnalytics = async (repositoryId: string) => {
  const response = await api.get(`/api/v1/analytics/repositories/${repositoryId}`);
  return response.data;
};

export const getSearchTrends = async (days: number = 7) => {
  const response = await api.get('/api/v1/search/trends', { params: { days } });
  return response.data;
};

// User API
export const login = async (credentials: { username: string; password: string }) => {
  const response = await api.post('/api/v1/auth/login', credentials);
  return response.data;
};

export const register = async (userData: {
  username: string;
  email: string;
  password: string;
}) => {
  const response = await api.post('/api/v1/auth/register', userData);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/api/v1/auth/me');
  return response.data;
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api; 