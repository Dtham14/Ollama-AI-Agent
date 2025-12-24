import { api } from './api';
import type { Session, CreateSessionRequest } from '../types';

export const sessionApi = {
  createSession: async (request: CreateSessionRequest): Promise<Session> => {
    const response = await api.post<Session>('/api/sessions', request);
    return response.data;
  },

  listSessions: async (limit?: number): Promise<Session[]> => {
    const response = await api.get<Session[]>('/api/sessions', {
      params: { limit },
    });
    return response.data;
  },

  getSession: async (sessionId: string): Promise<Session> => {
    const response = await api.get<Session>(`/api/sessions/${sessionId}`);
    return response.data;
  },
};
