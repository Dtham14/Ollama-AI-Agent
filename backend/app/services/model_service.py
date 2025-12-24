import httpx
from typing import List
from ..schemas.model import ModelInfo, ModelListResponse
from ..config import settings


class ModelService:
    """Service for managing Ollama models"""

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.current_model = settings.DEFAULT_MODEL

    async def list_models(self) -> ModelListResponse:
        """List all available Ollama models"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                data = response.json()

                models = [
                    ModelInfo(
                        name=model.get("name"),
                        size=model.get("size"),
                        modified=model.get("modified_at"),
                        id=model.get("digest")
                    )
                    for model in data.get("models", [])
                ]

                return ModelListResponse(
                    models=models,
                    current_model=self.current_model
                )
            except Exception as e:
                print(f"Error listing models: {e}")
                return ModelListResponse(models=[], current_model=self.current_model)

    def select_model(self, model_name: str) -> str:
        """Select a model to use"""
        self.current_model = model_name
        return model_name

    def get_current_model(self) -> str:
        """Get the currently selected model"""
        return self.current_model


# Singleton instance
model_service = ModelService()
