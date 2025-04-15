# services/metadata.py
from models.metadata import Metadata
from services.db_service import DatabaseService
from services.search_service import SearchService

# MetadataService handles the metadata operations, including saving and searching metadata.
class MetadataService:
    def __init__(self):
        """
        @summary: Initialize the MetadataService with database and search services.
        """
        self.db_service = DatabaseService()
        self.search_service = SearchService()

    def save_metadata(self, metadata: Metadata):
        """
        @summary: Save metadata to the database.
        @param metadata: The metadata object to save.
        @return: True if saved successfully, False otherwise.
        """
        db_result = self.db_service.save(metadata)
        if db_result:
            # Optionally update search index
            self.search_service.index_metadata(metadata)
            return True
        return False

    def search_metadata(self, query: str, limit: int, offset: int):
        """
        @summary: Search for metadata using the search service.
        @param query: The search query string.
        """
        return self.search_service.search(query, limit, offset)
