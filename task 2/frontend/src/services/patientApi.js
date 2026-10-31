import api from './api';

export const patientApi = {
  getAll: (search = '') => api.get('/patients', { params: search ? { search } : {} }),
  getById: (id) => api.get(`/patients/${id}`),
  create: (data) => api.post('/patients', data),
  update: (id, data) => api.put(`/patients/${id}`, data),
  delete: (id) => api.delete(`/patients/${id}`),
  analyze: (id) => api.post(`/patients/${id}/analyze`),
  getHealth: () => api.get('/health'),
};
