from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class Idea(Base):
    __tablename__ = "ideas"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # リレーション
    owner = relationship("User", back_populates="ideas")
    requirements = relationship("Requirement", back_populates="idea", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="idea", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="idea", cascade="all, delete-orphan")
    shares = relationship("Share", back_populates="idea", cascade="all, delete-orphan")

class Requirement(Base):
    __tablename__ = "requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"), nullable=False)
    content = Column(Text, nullable=False)
    llm_model = Column(String(50), nullable=False)  # 使用したLLMモデル
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーション
    idea = relationship("Idea", back_populates="requirements")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    position = Column(JSON)  # コメントの位置情報（オプション）
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーション
    idea = relationship("Idea", back_populates="comments")
    user = relationship("User", back_populates="comments")

class Bookmark(Base):
    __tablename__ = "bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    position = Column(JSON)  # ブックマークの位置情報
    note = Column(Text)  # ブックマークのメモ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーション
    idea = relationship("Idea", back_populates="bookmarks")
    user = relationship("User", back_populates="bookmarks")

class Share(Base):
    __tablename__ = "shares"
    
    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"), nullable=False)
    share_token = Column(String(255), unique=True, nullable=False)
    is_editable = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーション
    idea = relationship("Idea", back_populates="shares")