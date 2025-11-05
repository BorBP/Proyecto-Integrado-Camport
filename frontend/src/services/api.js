import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

// Interceptor para agregar el token JWT
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const authService = {
  login: async (username, password) => {
    const response = await axios.post(`${API_URL}/token/`, { username, password });
    if (response.data.access) {
      localStorage.setItem('token', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);
    }
    return response.data;
  },
  
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
  },
  
  getCurrentUser: async () => {
    const response = await api.get('/users/me/');
    return response.data;
  },
};

export const animalService = {
  getAll: async () => {
    const response = await api.get('/animales/');
    return response.data;
  },
  
  getOne: async (id) => {
    const response = await api.get(`/animales/${id}/`);
    return response.data;
  },
  
  create: async (data) => {
    const response = await api.post('/animales/', data);
    return response.data;
  },
  
  update: async (id, data) => {
    const response = await api.put(`/animales/${id}/`, data);
    return response.data;
  },
  
  delete: async (id) => {
    await api.delete(`/animales/${id}/`);
  },
};

export const geocercaService = {
  getActiva: async () => {
    const response = await api.get('/geocercas/activa/');
    return response.data;
  },
  
  getAll: async () => {
    const response = await api.get('/geocercas/');
    return response.data;
  },
  
  create: async (data) => {
    const response = await api.post('/geocercas/', data);
    return response.data;
  },
  
  update: async (id, data) => {
    const response = await api.put(`/geocercas/${id}/`, data);
    return response.data;
  },
};

export const alertaService = {
  getAll: async () => {
    const response = await api.get('/alertas-usuario/');
    return response.data;
  },
  
  getNoLeidas: async () => {
    const response = await api.get('/alertas-usuario/no_leidas/');
    return response.data;
  },
  
  marcarLeida: async (id) => {
    const response = await api.post(`/alertas-usuario/${id}/marcar_leido/`);
    return response.data;
  },
};

export const userService = {
  getAll: async () => {
    const response = await api.get('/users/');
    return response.data;
  },
  
  create: async (data) => {
    const response = await api.post('/users/', data);
    return response.data;
  },
  
  update: async (id, data) => {
    const response = await api.put(`/users/${id}/`, data);
    return response.data;
  },
  
  delete: async (id) => {
    await api.delete(`/users/${id}/`);
  },
};

export default api;
