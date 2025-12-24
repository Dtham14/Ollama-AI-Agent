import React from 'react';
import { Send } from 'lucide-react';
import { cn } from '../../utils/cn';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSend, disabled }) => {
  const [input, setInput] = React.useState('');
  const textareaRef = React.useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);

    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  };

  return (
    <form onSubmit={handleSubmit} className="border-t border-gray-200 bg-white p-4">
      <div className="flex gap-3 items-end">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about music theory..."
          disabled={disabled}
          rows={1}
          className={cn(
            'flex-1 resize-none rounded-lg border border-gray-300 px-4 py-3',
            'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
            'disabled:bg-gray-100 disabled:cursor-not-allowed',
            'max-h-32 overflow-y-auto'
          )}
        />
        <button
          type="submit"
          disabled={disabled || !input.trim()}
          className={cn(
            'flex-shrink-0 p-3 rounded-lg bg-primary-600 text-white',
            'hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500',
            'disabled:bg-gray-300 disabled:cursor-not-allowed',
            'transition-colors'
          )}
        >
          <Send size={20} />
        </button>
      </div>
      <p className="text-xs text-gray-500 mt-2">
        Press Enter to send, Shift + Enter for new line
      </p>
    </form>
  );
};
