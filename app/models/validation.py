from pydantic import BaseModel, Field, conlist
from typing import List, Optional
from datetime import datetime

# Define the Attribute model
class Attribute(BaseModel):
    name: str
    type: str
    nullable: bool

    class Config:
        """""""
        min_anystr_length = 1
        anystr_strip_whitespace = True

# Define the MetadataDetails model
class MetadataDetails(BaseModel):
    name: str
    description: str
    attributes: List[Attribute]

    class Config:
        min_anystr_length = 1
        anystr_strip_whitespace = True

# Define the MetadataIn model
class MetadataIn(BaseModel):
    source_type: str = Field(..., example="MySQL")
    source_id: str = Field(..., example="db1.table1")
    metadata: MetadataDetails
    tags: List[str] = Field(..., example=["sensitive", "user_data"])
    timestamp: datetime
    tenant_id: str = Field(..., example="tenant_123")

    class Config:
        min_anystr_length = 1
        anystr_strip_whitespace = True

    # You can add additional validation if needed
    @classmethod
    def validate_metadata(cls, metadata: dict):
        # Perform custom validation logic here, if necessary
        pass
