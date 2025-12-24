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
  updateSession: (sessionId: string, title: string) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
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

  updateSession: async (sessionId, title) => {
    try {
      const updatedSession = await sessionApi.updateSession(sessionId, title);
      set((state) => ({
        sessions: state.sessions.map((s) =>
          s.id === sessionId ? updatedSession : s
        ),
      }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to update session';
      set({ error: errorMessage });
      throw error;
    }
  },

  deleteSession: async (sessionId) => {
    try {
      await sessionApi.deleteSession(sessionId);
      set((state) => ({
        sessions: state.sessions.filter((s) => s.id !== sessionId),
      }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to delete session';
      set({ error: errorMessage });
      throw error;
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
