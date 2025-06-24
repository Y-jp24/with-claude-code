from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .requirement import Requirement

class IdeaBase(BaseModel):
    title: str
    content: str

class IdeaCreate(IdeaBase):
    pass

class IdeaUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class IdeaInDBBase(IdeaBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Idea(IdeaInDBBase):
    pass

class IdeaWithDetails(IdeaInDBBase):
    requirements: List[Dict[str, Any]] = []
    comments: List['Comment'] = []
    bookmarks: List['Bookmark'] = []

# コメント
class CommentBase(BaseModel):
    content: str
    position: Optional[Dict[str, Any]] = None

class CommentCreate(CommentBase):
    idea_id: int

class Comment(CommentBase):
    id: int
    idea_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ブックマーク
class BookmarkBase(BaseModel):
    position: Dict[str, Any]
    note: Optional[str] = None

class BookmarkCreate(BookmarkBase):
    idea_id: int

class Bookmark(BookmarkBase):
    id: int
    idea_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 共有
class ShareCreate(BaseModel):
    idea_id: int
    is_editable: bool = False
    expires_at: Optional[datetime] = None

class Share(BaseModel):
    id: int
    idea_id: int
    share_token: str
    is_editable: bool
    expires_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True