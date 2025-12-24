import { api } from './api';
import type { DocumentMetadata, DocumentListResponse } from '../types/document';

export const documentApi = {
  uploadDocument: async (
    file: File,
    category: string = 'Music Theory',
    tags: string = '',
    description?: string
  ): Promise<DocumentMetadata> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('category', category);
    formData.append('tags', tags);
    if (description) {
      formData.append('description', description);
    }

    const response = await api.post<DocumentMetadata>('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  listDocuments: async (limit?: number): Promise<DocumentListResponse> => {
    const response = await api.get<DocumentListResponse>('/api/documents', {
      params: { limit },
    });
    return response.data;
  },

  getDocument: async (documentId: string): Promise<DocumentMetadata> => {
    const response = await api.get<DocumentMetadata>(`/api/documents/${documentId}`);
    return response.data;
  },

  deleteDocument: async (documentId: string): Promise<void> => {
    await api.delete(`/api/documents/${documentId}`);
  },

  reembedDocument: async (documentId: string): Promise<{ message: string; chunk_count: number }> => {
    const response = await api.post(`/api/documents/${documentId}/reembed`);
    return response.data;
  },
};
