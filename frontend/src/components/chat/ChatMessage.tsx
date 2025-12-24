import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot, ChevronDown, ChevronUp } from 'lucide-react';
import type { Message } from '../../types';
import { cn } from '../../utils/cn';

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const [showSources, setShowSources] = React.useState(false);
  const isUser = message.role === 'user';

  return (
    <div
      className={cn(
        'flex gap-3 p-4',
        isUser ? 'bg-white justify-end' : 'bg-gray-50 justify-start'
      )}
    >
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-gray-800 text-white">
          <Bot size={18} />
        </div>
      )}

      <div className={cn(
        'min-w-0',
        isUser ? 'max-w-[80%]' : 'flex-1'
      )}>
        <div className={cn(
          'prose prose-sm max-w-none',
          isUser && 'bg-blue-100 text-black rounded-lg px-4 py-2'
        )}>
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>

        {message.sources && message.sources.length > 0 && (
          <div className="mt-3">
            <button
              onClick={() => setShowSources(!showSources)}
              className="flex items-center gap-1 text-sm text-gray-600 hover:text-gray-900 transition-colors"
            >
              {showSources ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
              <span>{message.sources.length} sources</span>
            </button>

            {showSources && (
              <div className="mt-2 space-y-2">
                {message.sources.map((source, idx) => (
                  <div
                    key={idx}
                    className="p-3 bg-white border border-gray-200 rounded-lg text-sm"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-medium text-gray-900">
                        {source.source}
                      </span>
                      <span className="text-xs text-gray-500">
                        Score: {source.score.toFixed(3)}
                      </span>
                    </div>
                    <p className="text-gray-600 text-xs line-clamp-2">
                      {source.content}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-primary-600 text-white">
          <User size={18} />
        </div>
      )}
    </div>
  );
};
