import { create } from 'zustand';
import type { ModelInfo } from '../types';
import { modelApi } from '../services';

interface ModelState {
  models: ModelInfo[];
  currentModel: string;
  isLoading: boolean;
  error: string | null;

  // Actions
  loadModels: () => Promise<void>;
  selectModel: (modelName: string) => Promise<void>;
}

export const useModelStore = create<ModelState>((set) => ({
  models: [],
  currentModel: 'meta-llama/Llama-3.2-3B-Instruct',
  isLoading: false,
  error: null,

  loadModels: async () => {
    set({ isLoading: true, error: null });

    try {
      const response = await modelApi.listModels();
      set({ models: response.models, currentModel: response.current_model });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to load models';
      set({ error: errorMessage });
    } finally {
      set({ isLoading: false });
    }
  },

  selectModel: async (modelName) => {
    set({ isLoading: true, error: null });

    try {
      await modelApi.selectModel({ model_name: modelName });
      set({ currentModel: modelName });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to select model';
      set({ error: errorMessage });
    } finally {
      set({ isLoading: false });
    }
  },
}));
