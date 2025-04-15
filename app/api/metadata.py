from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import ValidationError
from datetime import datetime
from typing import List
import logging

from ..models.validation import MetadataIn  # Import MetadataIn from validation
from ..services.metadata import MetadataService  # Service to handle business logic
from ..services.auth_service import get_current_user  # JWT Authentication

# Initialize logging
logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/metadata", status_code=status.HTTP_201_CREATED)
async def ingest_metadata(metadata: MetadataIn, user: str = Depends(get_current_user)):
    """
    @summary: Ingest metadata into the system.
    @param metadata: The metadata object to be ingested.
    @param user: The current user making the request.
    @return: A success message if ingestion is successful.
    @raises HTTPException: If there is a validation error or other issues during ingestion.
    """
    try:
        logger.info(f"User '{user}' is attempting to ingest metadata: {metadata.source_id}")

        # Validate the metadata input
        metadata_service = MetadataService()
        result = await metadata_service.ingest_metadata(metadata)

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

@router.get("/metadata/search", response_model=List[MetadataIn])
async def search_metadata(query: str, limit: int = 10, offset: int = 0, user: str = Depends(get_current_user)):
    """
    @summary: Search for metadata based on a query string.
    @param query: The search query string.
    @param limit: The maximum number of results to return.
    @param offset: The offset for pagination.
    @param user: The current user making the request.
    @return: A list of metadata objects matching the search query.
    @raises HTTPException: If there is an error during the search.
    """
    try:
        logger.info(f"User '{user}' is searching for metadata with query: {query}")

        # Validate the search parameters
        metadata_service = MetadataService()
        results = await metadata_service.search_metadata(query, limit, offset)

        logger.info(f"Search successful for query: {query}, found {len(results)} results")

        return results

    except Exception as e:
        logger.error(f"Error during metadata search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
