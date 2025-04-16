from fastapi import APIRouter, HTTPException, Depends, Query, status
from pydantic import ValidationError
from datetime import datetime
from typing import List
import logging
from models.validation import MetadataIn, SearchResponse, MetadataSearchResult
from services.metadata_service import MetadataService
from services.auth_service import AuthService, oauth2_scheme
from utils.helpers import Helpers

# Initialize logging
logger = logging.getLogger(__name__)
router = APIRouter()
auth_service = AuthService()

@router.post("/metadata", status_code=status.HTTP_201_CREATED)
async def ingest_metadata(metadata: MetadataIn, token: str = Depends(oauth2_scheme)):
    """
    :summary: Ingest metadata into the system.
    :param metadata: The metadata object to be ingested.
    :param token : JWT token
    :return: A success message if ingestion is successful.
    :raises HTTPException: If there is a validation error or other issues during ingestion.
    """
    try:
        current_user = auth_service.verify_token(token)
        logger.info(f"User '{current_user}' is attempting to ingest metadata: {metadata.source_id}")

        # Validate the metadata input
        metadata_service = MetadataService()
        asset_id = Helpers.generate(
            source_type=metadata.source_type,
            source_id=metadata.source_id,
            tenant_id=metadata.tenant_id
        )
        status = metadata_service.ingest_metadata(asset_id, metadata)
        if not status:
            raise HTTPException(status_code=400, detail="Failed to ingest metadata")
        logger.info(f"Metadata ingestion successful for source_id: {metadata.source_id}")

        return {"status": "success", "message": "Metadata ingested successfully", "asset_id": asset_id}

    except ValidationError as e:
        # Log validation error
        logger.error(f"Validation error during metadata ingestion: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Validation Error: {e}")
    except HTTPException as e:
        raise e
    except Exception as e:
        # Catch any other exceptions and log the error
        logger.error(f"Error during metadata ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/metadata/search", response_model=SearchResponse)
async def search_metadata(query: str = Query(..., description="Search query to match asset_id or name"),
    limit: int = Query(10, ge=1, le=100, description="Limit the number of results returned"),
    offset: int = Query(0, ge=0, description="Offset for pagination"), token: str = Depends(oauth2_scheme)):

    try:
        current_user = auth_service.verify_token(token)
        logger.info(f"User '{current_user}' is searching with query: {query}, limit: {limit}, offset: {offset}")

        # Handle empty query case
        if not query.strip():
            # Return empty results instead of raising an error
            return SearchResponse(
                results=[],
                total=0,
                limit=limit,
                offset=offset
            )
            
        # Continue with normal search...
        metadata_service = MetadataService()
        search_results = await metadata_service.search_metadata(query, limit, offset)
        
        return search_results
        
    except Exception as e:
        logger.error(f"Error during metadata search: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during metadata search: {str(e)}")
