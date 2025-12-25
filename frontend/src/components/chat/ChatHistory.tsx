import React from 'react';
import { ChatMessage } from './ChatMessage';
import type { Message } from '../../types';
import { Loader2 } from 'lucide-react';

interface ChatHistoryProps {
  messages: Message[];
  isLoading?: boolean;
}

export const ChatHistory: React.FC<ChatHistoryProps> = ({ messages, isLoading }) => {
  const scrollRef = React.useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  React.useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div
      ref={scrollRef}
      className="flex-1 overflow-y-auto scrollbar-hide"
    >
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full text-gray-500">
          <div className="text-center">
            <h3 className="text-lg font-semibold mb-2">
              Welcome to Classical Music Q&A
            </h3>
            <p className="text-sm">
              Ask me about classical composers, their lives, works, and contributions to music!
            </p>
          </div>
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
          {isLoading && (
            <div className="flex gap-3 p-4 bg-gray-50">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-800 text-white flex items-center justify-center">
                <Loader2 size={18} className="animate-spin" />
              </div>
              <div className="flex-1">
                <p className="text-gray-600">Thinking...</p>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};
