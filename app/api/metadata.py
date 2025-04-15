from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import ValidationError
from datetime import datetime
from typing import List
import logging

from ..models.validation import MetadataIn  # Import MetadataIn from validation
from ..services.metadata import MetadataService  # Service to handle business logic
from ..services.auth_service import get_current_user  # JWT Authentication

# Set up logging
logger = logging.getLogger(__name__)
router = APIRouter()

# Route for Ingesting Metadata
@router.post("/metadata", status_code=status.HTTP_201_CREATED)
async def ingest_metadata(metadata: MetadataIn, user: str = Depends(get_current_user)):
    try:
        # Log metadata ingestion attempt
        logger.info(f"User '{user}' is attempting to ingest metadata: {metadata.source_id}")

        # Pass the metadata to the MetadataService to handle business logic
        metadata_service = MetadataService()
        result = await metadata_service.ingest_metadata(metadata)

        # Log successful ingestion
        logger.info(f"Metadata ingestion successful for source_id: {metadata.source_id}")

        return {"status": "success", "message": "Metadata ingested successfully", "data": result}

    except ValidationError as e:
        # Log validation error
        logger.error(f"Validation error during metadata ingestion: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Validation Error: {e}")

    except Exception as e:
        # Catch any other exceptions and log the error
        logger.error(f"Error during metadata ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Route for Searching Metadata
@router.get("/metadata/search", response_model=List[MetadataIn])
async def search_metadata(query: str, limit: int = 10, offset: int = 0, user: str = Depends(get_current_user)):
    try:
        # Log search query attempt
        logger.info(f"User '{user}' is searching for metadata with query: {query}")

        # Pass the search query to the service to perform the search
        metadata_service = MetadataService()
        results = await metadata_service.search_metadata(query, limit, offset)

        # Log successful search
        logger.info(f"Search successful for query: {query}, found {len(results)} results")

        return results

    except Exception as e:
        # Catch any exceptions during search and log
        logger.error(f"Error during metadata search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
