export interface Session {
  id: string;
  title: string | null;
  created_at: string;
  updated_at: string;
  message_count: number;
  model_name: string;
}

export interface CreateSessionRequest {
  title?: string;
  model_name?: string;
}
