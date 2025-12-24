import { create } from 'zustand';
import type { Session } from '../types';
import { sessionApi } from '../services';

interface SessionState {
  sessions: Session[];
  isLoading: boolean;
  error: string | null;

  // Actions
  loadSessions: () => Promise<void>;
  createSession: (title?: string, modelName?: string) => Promise<Session>;
  refreshSessions: () => Promise<void>;
}

export const useSessionStore = create<SessionState>((set) => ({
  sessions: [],
  isLoading: false,
  error: null,

  loadSessions: async () => {
    set({ isLoading: true, error: null });

    try {
      const sessions = await sessionApi.listSessions();
      set({ sessions });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to load sessions';
      set({ error: errorMessage });
    } finally {
      set({ isLoading: false });
    }
  },

  createSession: async (title, modelName) => {
    set({ isLoading: true, error: null });

    try {
      const session = await sessionApi.createSession({ title, model_name: modelName });
      set((state) => ({ sessions: [session, ...state.sessions] }));
      return session;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to create session';
      set({ error: errorMessage });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },

  refreshSessions: async () => {
    try {
      const sessions = await sessionApi.listSessions();
      set({ sessions });
    } catch (error) {
      console.error('Failed to refresh sessions:', error);
    }
  },
}));
