import React from 'react';
import { FileText, Edit2, Check, X } from 'lucide-react';
import { ChatHistory } from './ChatHistory';
import { ChatInput } from './ChatInput';
import { DocumentPanel } from '../documents/DocumentPanel';
import { useChatStore, useSessionStore } from '../../stores';

export const ChatContainer: React.FC = () => {
  const [isDocumentPanelOpen, setIsDocumentPanelOpen] = React.useState(false);
  const [isEditingTitle, setIsEditingTitle] = React.useState(false);
  const [editTitle, setEditTitle] = React.useState('');
  const { messages, isLoading, sendMessage, currentSessionId } = useChatStore();
  const { sessions, updateSession, loadSessions } = useSessionStore();

  const handleSendMessage = async (content: string) => {
    await sendMessage(content);
  };

  const currentSession = sessions.find(s => s.id === currentSessionId);
  const sessionTitle = currentSession?.title || 'New Conversation';

  const handleStartEdit = () => {
    if (!currentSessionId) {
      alert('Please send a message first to create a session');
      return;
    }
    setEditTitle(sessionTitle);
    setIsEditingTitle(true);
  };

  const handleSaveTitle = async () => {
    if (!currentSessionId || !editTitle.trim()) {
      return;
    }
    try {
      await updateSession(currentSessionId, editTitle.trim());
      await loadSessions();
      setIsEditingTitle(false);
    } catch (error) {
      alert('Failed to update title');
    }
  };

  const handleCancelEdit = () => {
    setIsEditingTitle(false);
    setEditTitle('');
  };

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      <div className="flex-shrink-0 border-b border-gray-200 bg-white px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex-1 min-w-0 mr-4">
            {currentSessionId ? (
              <div className="flex items-center gap-2">
                {isEditingTitle ? (
                  <>
                    <input
                      type="text"
                      value={editTitle}
                      onChange={(e) => setEditTitle(e.target.value)}
                      className="text-xl font-semibold text-gray-900 border-b-2 border-blue-500 focus:outline-none bg-transparent px-1"
                      autoFocus
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') handleSaveTitle();
                        if (e.key === 'Escape') handleCancelEdit();
                      }}
                    />
                    <button
                      onClick={handleSaveTitle}
                      className="p-1 hover:bg-green-100 rounded text-green-600"
                      title="Save"
                    >
                      <Check size={18} />
                    </button>
                    <button
                      onClick={handleCancelEdit}
                      className="p-1 hover:bg-gray-100 rounded text-gray-600"
                      title="Cancel"
                    >
                      <X size={18} />
                    </button>
                  </>
                ) : (
                  <>
                    <h1 className="text-xl font-semibold text-gray-900 truncate">
                      {sessionTitle}
                    </h1>
                    <button
                      onClick={handleStartEdit}
                      className="p-1 hover:bg-gray-100 rounded text-gray-600 flex-shrink-0"
                      title="Rename conversation"
                    >
                      <Edit2 size={18} />
                    </button>
                  </>
                )}
              </div>
            ) : (
              <h1 className="text-xl font-semibold text-gray-900">
                Classical Music Q&A
              </h1>
            )}
            <p className="text-sm text-gray-600">
              Powered by HuggingFace & LangChain
            </p>
          </div>
          <button
            onClick={() => setIsDocumentPanelOpen(true)}
            className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <FileText size={18} />
            <span>Documents</span>
          </button>
        </div>
      </div>

      {/* Chat History */}
      <ChatHistory messages={messages} isLoading={isLoading} />

      {/* Input */}
      <div className="flex-shrink-0">
        <ChatInput onSend={handleSendMessage} disabled={isLoading} />
      </div>

      {/* Document Panel */}
      <DocumentPanel
        isOpen={isDocumentPanelOpen}
        onClose={() => setIsDocumentPanelOpen(false)}
      />
    </div>
  );
};
