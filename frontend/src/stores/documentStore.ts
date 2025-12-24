import { create } from 'zustand';
import type { DocumentMetadata } from '../types/document';
import { documentApi } from '../services/documentApi';

interface DocumentState {
  documents: DocumentMetadata[];
  isLoading: boolean;
  isUploading: boolean;
  error: string | null;

  // Actions
  loadDocuments: () => Promise<void>;
  uploadDocument: (file: File, category?: string, tags?: string, description?: string) => Promise<DocumentMetadata>;
  deleteDocument: (documentId: string) => Promise<void>;
  refreshDocuments: () => Promise<void>;
}

export const useDocumentStore = create<DocumentState>((set) => ({
  documents: [],
  isLoading: false,
  isUploading: false,
  error: null,

  loadDocuments: async () => {
    set({ isLoading: true, error: null });

    try {
      const response = await documentApi.listDocuments();
      set({ documents: response.documents });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to load documents';
      set({ error: errorMessage });
    } finally {
      set({ isLoading: false });
    }
  },

  uploadDocument: async (file, category, tags, description) => {
    set({ isUploading: true, error: null });

    try {
      const document = await documentApi.uploadDocument(file, category, tags, description);
      set((state) => ({ documents: [document, ...state.documents] }));
      return document;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to upload document';
      set({ error: errorMessage });
      throw error;
    } finally {
      set({ isUploading: false });
    }
  },

  deleteDocument: async (documentId) => {
    set({ isLoading: true, error: null });

    try {
      await documentApi.deleteDocument(documentId);
      set((state) => ({
        documents: state.documents.filter((doc) => doc.id !== documentId),
      }));
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to delete document';
      set({ error: errorMessage });
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },

  refreshDocuments: async () => {
    try {
      const response = await documentApi.listDocuments();
      set({ documents: response.documents });
    } catch (error) {
      console.error('Failed to refresh documents:', error);
    }
  },
}));
