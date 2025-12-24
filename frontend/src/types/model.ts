export interface ModelInfo {
  name: string;
  size?: string;
  modified?: string;
  id?: string;
}

export interface ModelListResponse {
  models: ModelInfo[];
  current_model: string;
}

export interface ModelSelection {
  model_name: string;
}
