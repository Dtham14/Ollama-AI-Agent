import React from 'react';
import { Plus, MessageSquare, ChevronLeft, ChevronRight, Trash2, Edit2, Check, X } from 'lucide-react';
import { useSessionStore, useChatStore } from '../../stores';
import { cn } from '../../utils/cn';

export const SessionSidebar: React.FC = () => {
  const [isOpen, setIsOpen] = React.useState(true);
  const [editingId, setEditingId] = React.useState<string | null>(null);
  const [editTitle, setEditTitle] = React.useState('');
  const { sessions, loadSessions, createSession, updateSession, deleteSession } = useSessionStore();
  const { currentSessionId, loadHistory, clearMessages, setCurrentSession } = useChatStore();

  React.useEffect(() => {
    loadSessions();
  }, [loadSessions]);

  const handleNewChat = async () => {
    // Check if current session has unsaved messages
    const { messages, currentSessionId } = useChatStore.getState();

    if (messages.length > 0 && !currentSessionId) {
      const confirmSwitch = confirm(
        'You have unsaved messages in the current chat. Starting a new chat will discard them. Continue?'
      );
      if (!confirmSwitch) {
        return;
      }
    }

    clearMessages();
    setCurrentSession(null);
  };

  const handleSelectSession = async (sessionId: string) => {
    // Check if current session has unsaved messages
    const { messages, currentSessionId } = useChatStore.getState();

    if (messages.length > 0 && !currentSessionId && sessionId !== currentSessionId) {
      const confirmSwitch = confirm(
        'You have unsaved messages in the current chat. Switching to another chat will discard them. Continue?'
      );
      if (!confirmSwitch) {
        return;
      }
    }

    await loadHistory(sessionId);
  };

  const handleDeleteSession = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm('Are you sure you want to delete this conversation?')) {
      return;
    }

    try {
      await deleteSession(sessionId);
      // If we deleted the current session, clear the chat
      if (currentSessionId === sessionId) {
        clearMessages();
      }
    } catch (error) {
      alert('Failed to delete conversation. Please try again.');
    }
  };

  const handleStartEdit = (sessionId: string, currentTitle: string | null, e: React.MouseEvent) => {
    e.stopPropagation();
    setEditingId(sessionId);
    setEditTitle(currentTitle || 'New Conversation');
  };

  const handleSaveEdit = async (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!editTitle.trim()) {
      alert('Title cannot be empty');
      return;
    }

    try {
      await updateSession(sessionId, editTitle.trim());
      setEditingId(null);
    } catch (error) {
      alert('Failed to update title. Please try again.');
    }
  };

  const handleCancelEdit = (e: React.MouseEvent) => {
    e.stopPropagation();
    setEditingId(null);
    setEditTitle('');
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days === 0) return 'Today';
    if (days === 1) return 'Yesterday';
    if (days < 7) return `${days} days ago`;
    return date.toLocaleDateString();
  };

  return (
    <>
      <div
        className={cn(
          'flex-shrink-0 bg-gray-900 text-white transition-all duration-300',
          isOpen ? 'w-64' : 'w-0'
        )}
      >
        {isOpen && (
          <div className="h-full flex flex-col">
            {/* Header */}
            <div className="p-4 border-b border-gray-700">
              <button
                onClick={handleNewChat}
                className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors"
              >
                <Plus size={18} />
                <span>New Chat</span>
              </button>
            </div>

            {/* Sessions List */}
            <div className="flex-1 overflow-y-auto scrollbar-hide">
              {sessions.length === 0 ? (
                <div className="p-4 text-center text-gray-400 text-sm">
                  No sessions yet
                </div>
              ) : (
                <div className="p-2 space-y-1">
                  {sessions.map((session) => (
                    <div
                      key={session.id}
                      className={cn(
                        'w-full flex items-start gap-2 p-3 rounded-lg transition-colors group',
                        currentSessionId === session.id
                          ? 'bg-gray-700'
                          : 'hover:bg-gray-800'
                      )}
                    >
                      <button
                        onClick={() => handleSelectSession(session.id)}
                        className="flex items-start gap-2 flex-1 min-w-0 text-left"
                      >
                        <MessageSquare size={16} className="mt-1 flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          {editingId === session.id ? (
                            <input
                              type="text"
                              value={editTitle}
                              onChange={(e) => setEditTitle(e.target.value)}
                              onClick={(e) => e.stopPropagation()}
                              className="w-full text-sm bg-gray-600 text-white px-2 py-1 rounded border border-gray-500 focus:outline-none focus:border-blue-500"
                              autoFocus
                              onKeyDown={(e) => {
                                if (e.key === 'Enter') {
                                  handleSaveEdit(session.id, e as any);
                                } else if (e.key === 'Escape') {
                                  handleCancelEdit(e as any);
                                }
                              }}
                            />
                          ) : (
                            <p className="text-sm truncate">
                              {session.title || 'New Conversation'}
                            </p>
                          )}
                          <p className="text-xs text-gray-400 mt-1">
                            {formatDate(session.updated_at)} · {session.message_count} messages
                          </p>
                        </div>
                      </button>

                      {/* Action buttons */}
                      <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        {editingId === session.id ? (
                          <>
                            <button
                              onClick={(e) => handleSaveEdit(session.id, e)}
                              className="p-1 hover:bg-green-600 rounded text-green-400 hover:text-white"
                              title="Save"
                            >
                              <Check size={14} />
                            </button>
                            <button
                              onClick={handleCancelEdit}
                              className="p-1 hover:bg-gray-600 rounded text-gray-400 hover:text-white"
                              title="Cancel"
                            >
                              <X size={14} />
                            </button>
                          </>
                        ) : (
                          <>
                            <button
                              onClick={(e) => handleStartEdit(session.id, session.title, e)}
                              className="p-1 hover:bg-blue-600 rounded text-gray-400 hover:text-white"
                              title="Rename"
                            >
                              <Edit2 size={14} />
                            </button>
                            <button
                              onClick={(e) => handleDeleteSession(session.id, e)}
                              className="p-1 hover:bg-red-600 rounded text-gray-400 hover:text-white"
                              title="Delete"
                            >
                              <Trash2 size={14} />
                            </button>
                          </>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-gray-700">
              <p className="text-xs text-gray-400 text-center">
                Model: Llama 3.2 (HuggingFace)
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="absolute top-4 left-4 z-10 p-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors"
      >
        {isOpen ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
      </button>
    </>
  );
};
