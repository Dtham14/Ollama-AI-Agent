export interface DocumentMetadata {
  id: string;
  filename: string;
  original_filename: string;
  file_type: string;
  file_size: number;
  category: string;
  tags: string[];
  description: string | null;
  chunk_count: number;
  embedded: 'pending' | 'processing' | 'completed' | 'failed';
  uploaded_at: string;
  processed_at: string | null;
}

export interface DocumentListResponse {
  documents: DocumentMetadata[];
  total: number;
}

export interface DocumentUploadRequest {
  file: File;
  category?: string;
  tags?: string;
  description?: string;
}
