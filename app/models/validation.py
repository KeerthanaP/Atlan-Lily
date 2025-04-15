# models/validation.py
from pydantic import BaseModel, Field
from typing import List, Optional

class MetadataIn(BaseModel):
    asset_id: str
    name: str
    type: str
    description: Optional[str] = None
    tags: List[str] = []
    timestamp: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "asset_id": "db1.table1",
                "name": "Users",
                "type": "table",
                "description": "Contains user data",
                "tags": ["sensitive", "user_data"],
                "timestamp": "2025-04-15T12:00:00Z"
            }
        }
