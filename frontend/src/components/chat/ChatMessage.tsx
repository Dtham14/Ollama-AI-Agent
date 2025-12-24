import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot, ChevronDown, ChevronUp, Trash2 } from 'lucide-react';
import type { Message } from '../../types';
import { cn } from '../../utils/cn';
import { useChatStore } from '../../stores/chatStore';

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const [showSources, setShowSources] = React.useState(false);
  const [isDeleting, setIsDeleting] = React.useState(false);
  const deleteMessage = useChatStore((state) => state.deleteMessage);
  const isUser = message.role === 'user';

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this message?')) {
      return;
    }

    setIsDeleting(true);
    try {
      await deleteMessage(message.id);
    } catch (error) {
      console.error('Failed to delete message:', error);
      alert('Failed to delete message. Please try again.');
    } finally {
      setIsDeleting(false);
    }
  };

  return (
    <div
      className={cn(
        'flex gap-3 p-4 group relative hover:bg-gray-100',
        isUser ? 'bg-white justify-end' : 'bg-gray-50 justify-start',
        isDeleting && 'opacity-50 pointer-events-none'
      )}
    >
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-gray-800 text-white">
          <Bot size={18} />
        </div>
      )}

      <div className={cn(
        'min-w-0 flex-1',
        isUser && 'flex justify-end'
      )}>
        <div className="flex items-start gap-3 relative w-full">
          <div className={cn(
            'prose prose-sm max-w-none flex-1',
            isUser && 'bg-blue-100 text-black rounded-lg px-4 py-2'
          )}>
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>

          {/* Delete button - always visible on small opacity, full on hover */}
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className={cn(
              'opacity-30 group-hover:opacity-100 transition-all duration-200',
              'p-2 rounded-md hover:bg-red-50 text-gray-500 hover:text-red-600',
              'flex-shrink-0 self-start mt-1',
              'border border-transparent hover:border-red-200'
            )}
            title="Delete message"
          >
            <Trash2 size={14} />
          </button>
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
