import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1',
});

export const chatWithAgent = (message, model) => api.post('/chat/', { message, model });
export const uploadFiles = (files) => {
    const formData = new FormData();
    files.forEach(f => formData.append('files', f));
    return api.post('/documents/upload', formData);
};
// Fetch actual files in the "Brain"
export const getUploadedFiles = () => api.get('/documents/files'); 
export const getHistory = () => api.get('/history/');
export const clearHistory = () => api.delete('/history/clear');

export default api;