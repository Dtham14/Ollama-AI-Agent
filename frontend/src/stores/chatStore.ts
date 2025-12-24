import { create } from 'zustand';
import type { Message } from '../types';
import { chatApi } from '../services';

interface ChatState {
  messages: Message[];
  currentSessionId: string | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  setCurrentSession: (sessionId: string | null) => void;
  addMessage: (message: Message) => void;
  sendMessage: (content: string, includeSources?: boolean) => Promise<void>;
  loadHistory: (sessionId: string) => Promise<void>;
  deleteMessage: (messageId: string) => Promise<void>;
  clearMessages: () => void;
  setError: (error: string | null) => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  currentSessionId: null,
  isLoading: false,
  error: null,

  setCurrentSession: (sessionId) => set({ currentSessionId: sessionId }),

  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),

  sendMessage: async (content, includeSources = true) => {
    set({ isLoading: true, error: null });

    try {
      // Add user message immediately
      const userMessage: Message = {
        id: `temp-${Date.now()}`,
        role: 'user',
        content,
        created_at: new Date().toISOString(),
      };
      get().addMessage(userMessage);

      // Send to backend
      const response = await chatApi.sendMessage({
        message: content,
        session_id: get().currentSessionId || undefined,
        include_sources: includeSources,
      });

      // Update session ID if new session was created
      if (response.session_id && response.session_id !== get().currentSessionId) {
        set({ currentSessionId: response.session_id });
      }

      // Add assistant message
      get().addMessage(response.message);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to send message';
      set({ error: errorMessage });
    } finally {
      set({ isLoading: false });
    }
  },

  loadHistory: async (sessionId) => {
    set({ isLoading: true, error: null });

    try {
      const messages = await chatApi.getHistory(sessionId);
      set({ messages, currentSessionId: sessionId });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to load history';
      set({ error: errorMessage });
    } finally {
      set({ isLoading: false });
    }
  },

  deleteMessage: async (messageId) => {
    try {
      await chatApi.deleteMessage(messageId);
      // Remove message from local state
      set((state) => ({
        messages: state.messages.filter((msg) => msg.id !== messageId),
      }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to delete message';
      set({ error: errorMessage });
      throw error;
    }
  },

  clearMessages: () => set({ messages: [], currentSessionId: null }),

  setError: (error) => set({ error }),
}));
