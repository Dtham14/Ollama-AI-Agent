'use client'

import { SessionSidebar } from './SessionSidebar'
import { ChatHistory } from './ChatHistory'
import { ChatInput } from './ChatInput'

export function ChatContainer() {
  return (
    <div className="flex h-screen bg-gray-50">
      <SessionSidebar />

      <div className="flex-1 flex flex-col">
        <header className="bg-white border-b border-gray-200 px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Classical Music Assistant</h1>
          <p className="text-sm text-gray-600 mt-1">
            Ask me anything about classical composers, works, and musical history
          </p>
        </header>

        <ChatHistory />
        <ChatInput />
      </div>
    </div>
  )
}
