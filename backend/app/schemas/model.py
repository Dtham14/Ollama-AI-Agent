from pydantic import BaseModel
from typing import Optional


class ModelInfo(BaseModel):
    name: str
    size: Optional[str] = None
    modified: Optional[str] = None
    id: Optional[str] = None


class ModelSelection(BaseModel):
    model_name: str


class ModelListResponse(BaseModel):
    models: list[ModelInfo]
    current_model: str
