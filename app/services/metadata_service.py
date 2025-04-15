# services/metadata.py
from models.metadata import Metadata
from services.db_service import DatabaseService
from services.search_service import SearchService

class MetadataService:
    def __init__(self):
        self.db_service = DatabaseService()
        self.search_service = SearchService()

    def save_metadata(self, metadata: Metadata):
        # Save to database (mock implementation)
        db_result = self.db_service.save(metadata)
        if db_result:
            # Optionally update search index
            self.search_service.index_metadata(metadata)
            return True
        return False

    def search_metadata(self, query: str, limit: int, offset: int):
        # Search from the search service (mock implementation)
        return self.search_service.search(query, limit, offset)
