from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class HomeItem(Base):
    __tablename__ = "home_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    link = Column(String(500))  # リンク先URL
    position_x = Column(Float, default=0)  # X座標
    position_y = Column(Float, default=0)  # Y座標
    width = Column(Float, default=200)  # 幅
    height = Column(Float, default=150)  # 高さ
    color = Column(String(7), default="#FFE4B5")  # 背景色（付箋の色）
    style = Column(JSON)  # その他のスタイル情報
    
    # リレーション
    user = relationship("User", back_populates="home_items")