import axios from 'axios';

const API_URL = process.env.NODE_ENV === 'production' 
    ? window.location.origin 
    : 'http://127.0.0.1:8000';

// Create axios instance with base URL
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add interceptor to add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Auth services
export const authService = {
    login: async (email, password) => {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);
        const response = await api.post('/token', formData);
        if (response.data.access_token) {
            localStorage.setItem('token', response.data.access_token);
        }
        return response.data;
    },

    register: async (userData) => {
        const response = await api.post('/users/', userData);
        return response.data;
    },

    logout: () => {
        localStorage.removeItem('token');
    },

    getCurrentUser: () => {
        return localStorage.getItem('token');
    },
};

// Protected API services
export const calculatorService = {
    // Add your calculator-specific API calls here
    calculate: async (data) => {
        const response = await api.post('/calculate/', data);
        return response.data;
    },
    
    // Get calculation history
    getHistory: async () => {
        const response = await api.get('/history/');
        return response.data;
    },
};

export default api;