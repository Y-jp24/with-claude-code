from pydantic import BaseModel
from datetime import datetime
from typing import Literal

class RequirementBase(BaseModel):
    content: str
    llm_model: Literal["openai", "google", "claude"]

class RequirementCreate(RequirementBase):
    idea_id: int

class RequirementGenerate(BaseModel):
    idea_id: int
    llm_model: Literal["openai", "google", "claude"]

class Requirement(RequirementBase):
    id: int
    idea_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True