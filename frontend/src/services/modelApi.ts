import { api } from './api';
import type { ModelListResponse, ModelSelection } from '../types';

export const modelApi = {
  listModels: async (): Promise<ModelListResponse> => {
    const response = await api.get<ModelListResponse>('/api/models');
    return response.data;
  },

  selectModel: async (selection: ModelSelection): Promise<{ model: string; message: string }> => {
    const response = await api.post('/api/models/select', selection);
    return response.data;
  },

  getCurrentModel: async (): Promise<{ model: string }> => {
    const response = await api.get('/api/models/current');
    return response.data;
  },
};
