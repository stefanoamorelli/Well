from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class InputUpdate(BaseModel):
    fields: Dict[str, Any] = Field(..., description="Fields to merge into receipt_input.yaml")

class StyleCreate(BaseModel):
    name: str = Field(..., description="Name of the style (without .json)")
    content: Dict[str, Any] = Field(..., description="JSON content of the style")

class GenerationRequest(BaseModel):
    input_fields: Optional[Dict[str, Any]] = None
    style: str = "table_noire"
