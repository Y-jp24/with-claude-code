from pydantic import BaseModel
from typing import Optional, Dict, Any

class HomeItemBase(BaseModel):
    title: str
    content: Optional[str] = None
    link: Optional[str] = None
    position_x: float = 0
    position_y: float = 0
    width: float = 200
    height: float = 150
    color: str = "#FFE4B5"
    style: Optional[Dict[str, Any]] = None

class HomeItemCreate(HomeItemBase):
    pass

class HomeItemUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    link: Optional[str] = None
    position_x: Optional[float] = None
    position_y: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    color: Optional[str] = None
    style: Optional[Dict[str, Any]] = None

class HomeItem(HomeItemBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True