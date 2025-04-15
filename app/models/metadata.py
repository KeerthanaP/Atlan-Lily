from sqlalchemy import Column, String, Integer, JSON, DateTime
from app.database import Base
from datetime import datetime
import uuid

class MetadataDBModel(Base):
    __tablename__ = "metadata"
    
    asset_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    type = Column(String)
    tags = Column(JSON, default={})
    version = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
