'use client'

import { useEffect, useState } from 'react'
import { useSessionStore } from '@/stores/sessionStore'
import { useChatStore } from '@/stores/chatStore'
import { Plus, MessageSquare, Trash2, Edit2, Check, X } from 'lucide-react'

export function SessionSidebar() {
  const { sessions, loadSessions, createSession, updateSession, deleteSession } = useSessionStore()
  const { currentSessionId, setCurrentSession, loadHistory, clearMessages } = useChatStore()
  const [editingId, setEditingId] = useState<string | null>(null)
  const [editTitle, setEditTitle] = useState('')

  useEffect(() => {
    loadSessions()
  }, [loadSessions])

  const handleNewSession = async () => {
    try {
      const newSession = await createSession('New Chat')
      setCurrentSession(newSession.id)
      clearMessages()
    } catch (error) {
      console.error('Failed to create session:', error)
    }
  }

  const handleSelectSession = async (sessionId: string) => {
    if (sessionId === currentSessionId) return

    try {
      await loadHistory(sessionId)
      setCurrentSession(sessionId)
    } catch (error) {
      console.error('Failed to load session:', error)
    }
  }

  const handleDeleteSession = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation()

    if (!confirm('Delete this chat session?')) return

    try {
      await deleteSession(sessionId)
      if (sessionId === currentSessionId) {
        setCurrentSession(null)
        clearMessages()
      }
    } catch (error) {
      console.error('Failed to delete session:', error)
    }
  }

  const handleStartEdit = (sessionId: string, currentTitle: string | null, e: React.MouseEvent) => {
    e.stopPropagation()
    setEditingId(sessionId)
    setEditTitle(currentTitle || 'Untitled Chat')
  }

  const handleSaveEdit = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation()

    try {
      await updateSession(sessionId, editTitle)
      setEditingId(null)
    } catch (error) {
      console.error('Failed to update session:', error)
    }
  }

  const handleCancelEdit = (e: React.MouseEvent) => {
    e.stopPropagation()
    setEditingId(null)
  }

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col h-full">
      <div className="p-4 border-b border-gray-700">
        <button
          onClick={handleNewSession}
          className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
        >
          <Plus size={20} />
          New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {sessions.length === 0 ? (
          <div className="p-4 text-center text-gray-400 text-sm">
            No chat sessions yet
          </div>
        ) : (
          <div className="space-y-1 p-2">
            {sessions.map((session) => (
              <div
                key={session.id}
                onClick={() => handleSelectSession(session.id)}
                className={`group flex items-center gap-2 p-3 rounded-lg cursor-pointer transition-colors ${
                  session.id === currentSessionId
                    ? 'bg-gray-700'
                    : 'hover:bg-gray-800'
                }`}
              >
                <MessageSquare size={16} className="flex-shrink-0 text-gray-400" />

                {editingId === session.id ? (
                  <div className="flex-1 flex items-center gap-1" onClick={(e) => e.stopPropagation()}>
                    <input
                      type="text"
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      className="flex-1 bg-gray-800 text-white text-sm px-2 py-1 rounded border border-gray-600 focus:outline-none focus:border-blue-500"
                      autoFocus
                    />
                    <button
                      onClick={(e) => handleSaveEdit(session.id, e)}
                      className="text-green-500 hover:text-green-400"
                    >
                      <Check size={16} />
                    </button>
                    <button
                      onClick={handleCancelEdit}
                      className="text-red-500 hover:text-red-400"
                    >
                      <X size={16} />
                    </button>
                  </div>
                ) : (
                  <>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium truncate">
                        {session.title || 'Untitled Chat'}
                      </div>
                      <div className="text-xs text-gray-400">
                        {session.messageCount} messages
                      </div>
                    </div>

                    <div className="flex-shrink-0 flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button
                        onClick={(e) => handleStartEdit(session.id, session.title, e)}
                        className="text-gray-400 hover:text-white p-1"
                      >
                        <Edit2 size={14} />
                      </button>
                      <button
                        onClick={(e) => handleDeleteSession(session.id, e)}
                        className="text-gray-400 hover:text-red-400 p-1"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="p-4 border-t border-gray-700 text-xs text-gray-400">
        <p>Classical Music AI</p>
        <p className="mt-1">Powered by Llama 3.2-3B</p>
      </div>
    </div>
  )
}
