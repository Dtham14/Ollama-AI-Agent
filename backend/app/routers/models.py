from fastapi import APIRouter, HTTPException

from ..schemas.model import ModelListResponse, ModelSelection
from ..services.model_service import model_service

router = APIRouter(prefix="/api/models", tags=["models"])


@router.get("", response_model=ModelListResponse)
async def list_models():
    """List all available Ollama models"""
    return await model_service.list_models()


@router.post("/select")
async def select_model(selection: ModelSelection):
    """Select which model to use"""
    model_name = model_service.select_model(selection.model_name)
    return {"model": model_name, "message": f"Model switched to {model_name}"}


@router.get("/current")
async def get_current_model():
    """Get the currently selected model"""
    return {"model": model_service.get_current_model()}
