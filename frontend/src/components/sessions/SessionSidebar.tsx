import React from 'react';
import { Plus, MessageSquare, ChevronLeft, ChevronRight } from 'lucide-react';
import { useSessionStore, useChatStore } from '../../stores';
import { cn } from '../../utils/cn';

export const SessionSidebar: React.FC = () => {
  const [isOpen, setIsOpen] = React.useState(true);
  const { sessions, loadSessions, createSession } = useSessionStore();
  const { currentSessionId, loadHistory, clearMessages } = useChatStore();

  React.useEffect(() => {
    loadSessions();
  }, [loadSessions]);

  const handleNewChat = async () => {
    clearMessages();
  };

  const handleSelectSession = async (sessionId: string) => {
    await loadHistory(sessionId);
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
                    <button
                      key={session.id}
                      onClick={() => handleSelectSession(session.id)}
                      className={cn(
                        'w-full flex items-start gap-2 p-3 rounded-lg text-left transition-colors',
                        currentSessionId === session.id
                          ? 'bg-gray-700'
                          : 'hover:bg-gray-800'
                      )}
                    >
                      <MessageSquare size={16} className="mt-1 flex-shrink-0" />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm truncate">
                          {session.title || 'New Conversation'}
                        </p>
                        <p className="text-xs text-gray-400">
                          {formatDate(session.updated_at)} · {session.message_count} messages
                        </p>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-gray-700">
              <p className="text-xs text-gray-400 text-center">
                Model: llama3.2
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
