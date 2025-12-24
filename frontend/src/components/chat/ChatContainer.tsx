import React from 'react';
import { FileText } from 'lucide-react';
import { ChatHistory } from './ChatHistory';
import { ChatInput } from './ChatInput';
import { DocumentPanel } from '../documents/DocumentPanel';
import { useChatStore } from '../../stores';

export const ChatContainer: React.FC = () => {
  const [isDocumentPanelOpen, setIsDocumentPanelOpen] = React.useState(false);
  const { messages, isLoading, sendMessage } = useChatStore();

  const handleSendMessage = async (content: string) => {
    await sendMessage(content);
  };

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      <div className="flex-shrink-0 border-b border-gray-200 bg-white px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">
              Music Theory Q&A
            </h1>
            <p className="text-sm text-gray-600">
              Powered by Ollama & LangChain
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
