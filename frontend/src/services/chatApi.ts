import { api } from './api';
import type { ChatRequest, ChatResponse, Message } from '../types';

export const chatApi = {
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/api/chat/message', request);
    return response.data;
  },

  getHistory: async (sessionId: string, limit?: number): Promise<Message[]> => {
    const response = await api.get<Message[]>(`/api/chat/history/${sessionId}`, {
      params: { limit },
    });
    return response.data;
  },

  deleteHistory: async (sessionId: string): Promise<void> => {
    await api.delete(`/api/chat/history/${sessionId}`);
  },
};
