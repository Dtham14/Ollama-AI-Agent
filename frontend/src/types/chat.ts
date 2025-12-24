export interface SourceCitation {
  source: string;
  content: string;
  score: number;
  metadata?: Record<string, any>;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
  sources?: SourceCitation[];
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  include_sources?: boolean;
}

export interface ChatResponse {
  session_id: string;
  message: Message;
  model_used: string;
}
