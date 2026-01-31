import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1', // Use 127.0.0.1 instead of localhost
});

export const chatWithAgent = (message, model) => api.post('/chat/', { message, model });
export const uploadFiles = (files) => {
    const formData = new FormData();
    files.forEach(f => formData.append('files', f));
    return api.post('/documents/upload', formData);
};
export const getHistory = () => api.get('/history/');
export const clearHistory = () => api.delete('/history/clear');