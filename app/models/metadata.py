# models/metadata.py

from sqlalchemy import Column, String, Integer, JSON, DateTime
from models.database import Base
from datetime import datetime
import uuid

class MetadataDBModel(Base):
    __tablename__ = "metadata"
    
    metadata_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String, index=True)
    name = Column(String, index=True)
    type = Column(String)
    source_type = Column(String)  # Added for MySQL example
    source_id = Column(String)    # Added for MySQL example
    metadata_json = Column(JSON, default={})
    tags = Column(JSON, default=[])
    timestamp = Column(DateTime, default=datetime.utcnow)
    tenant_id = Column(String)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<MetadataDBModel(name={self.name}, type={self.type}, asset_id={self.asset_id})>"
