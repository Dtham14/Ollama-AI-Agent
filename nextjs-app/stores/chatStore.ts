import { create } from 'zustand'
import type { Message, ChatRequest, ChatResponse } from '@/types'

interface ChatState {
  messages: Message[]
  currentSessionId: string | null
  isLoading: boolean
  error: string | null

  setCurrentSession: (sessionId: string | null) => void
  addMessage: (message: Message) => void
  sendMessage: (content: string) => Promise<void>
  loadHistory: (sessionId: string) => Promise<void>
  clearMessages: () => void
  setError: (error: string | null) => void
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  currentSessionId: null,
  isLoading: false,
  error: null,

  setCurrentSession: (sessionId) => set({ currentSessionId: sessionId }),

  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),

  sendMessage: async (content) => {
    set({ isLoading: true, error: null })

    try {
      // Add user message immediately
      const userMessage: Message = {
        id: `temp-${Date.now()}`,
        sessionId: get().currentSessionId || '',
        role: 'user',
        content,
        createdAt: new Date(),
      }
      get().addMessage(userMessage)

      // Send to API
      const request: ChatRequest = {
        message: content,
        sessionId: get().currentSessionId || undefined,
      }

      const response = await fetch('/api/chat/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
      })

      if (!response.ok) {
        throw new Error('Failed to send message')
      }

      const data: ChatResponse = await response.json()

      // Update session ID if new session was created
      if (data.sessionId && data.sessionId !== get().currentSessionId) {
        set({ currentSessionId: data.sessionId })
      }

      // Add assistant message
      const assistantMessage: Message = {
        id: `${Date.now()}-assistant`,
        sessionId: data.sessionId,
        role: 'assistant',
        content: data.response,
        sources: data.sources,
        createdAt: new Date(),
      }
      get().addMessage(assistantMessage)
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to send message'
      set({ error: errorMessage })
    } finally {
      set({ isLoading: false })
    }
  },

  loadHistory: async (sessionId) => {
    set({ isLoading: true, error: null })

    try {
      const response = await fetch(`/api/chat/history/${sessionId}`)

      if (!response.ok) {
        throw new Error('Failed to load history')
      }

      const messages: Message[] = await response.json()
      set({ messages, currentSessionId: sessionId })
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to load history'
      set({ error: errorMessage })
    } finally {
      set({ isLoading: false })
    }
  },

  clearMessages: () => set({ messages: [], currentSessionId: null }),

  setError: (error) => set({ error }),
}))
