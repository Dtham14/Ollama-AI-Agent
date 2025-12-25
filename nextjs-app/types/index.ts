export interface Message {
  id: string
  sessionId: string
  role: 'user' | 'assistant'
  content: string
  sources?: SourceCitation[]
  createdAt: Date
}

export interface Session {
  id: string
  title: string | null
  createdAt: Date
  updatedAt: Date
  messageCount: number
  modelName: string
}

export interface SourceCitation {
  source: string
  content: string
  score: number
}

export interface ChatRequest {
  message: string
  sessionId?: string
}

export interface ChatResponse {
  response: string
  sessionId: string
  sources: SourceCitation[]
}
