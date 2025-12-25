import { create } from 'zustand'
import type { Session } from '@/types'

interface SessionState {
  sessions: Session[]
  isLoading: boolean
  error: string | null

  loadSessions: () => Promise<void>
  createSession: (title?: string) => Promise<Session>
  updateSession: (sessionId: string, title: string) => Promise<void>
  deleteSession: (sessionId: string) => Promise<void>
}

export const useSessionStore = create<SessionState>((set, get) => ({
  sessions: [],
  isLoading: false,
  error: null,

  loadSessions: async () => {
    set({ isLoading: true, error: null })

    try {
      const response = await fetch('/api/sessions')

      if (!response.ok) {
        throw new Error('Failed to load sessions')
      }

      const sessions: Session[] = await response.json()
      set({ sessions })
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to load sessions'
      set({ error: errorMessage })
    } finally {
      set({ isLoading: false })
    }
  },

  createSession: async (title) => {
    set({ isLoading: true, error: null })

    try {
      const response = await fetch('/api/sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title }),
      })

      if (!response.ok) {
        throw new Error('Failed to create session')
      }

      const session: Session = await response.json()
      set((state) => ({ sessions: [session, ...state.sessions] }))
      return session
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to create session'
      set({ error: errorMessage })
      throw error
    } finally {
      set({ isLoading: false })
    }
  },

  updateSession: async (sessionId, title) => {
    set({ isLoading: true, error: null })

    try {
      const response = await fetch(`/api/sessions/${sessionId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title }),
      })

      if (!response.ok) {
        throw new Error('Failed to update session')
      }

      const updatedSession: Session = await response.json()
      set((state) => ({
        sessions: state.sessions.map((s) =>
          s.id === sessionId ? updatedSession : s
        ),
      }))
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to update session'
      set({ error: errorMessage })
      throw error
    } finally {
      set({ isLoading: false })
    }
  },

  deleteSession: async (sessionId) => {
    set({ isLoading: true, error: null })

    try {
      const response = await fetch(`/api/sessions/${sessionId}`, {
        method: 'DELETE',
      })

      if (!response.ok) {
        throw new Error('Failed to delete session')
      }

      set((state) => ({
        sessions: state.sessions.filter((s) => s.id !== sessionId),
      }))
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : 'Failed to delete session'
      set({ error: errorMessage })
      throw error
    } finally {
      set({ isLoading: false })
    }
  },
}))
