# services/metadata.py
from models.metadata import MetadataDBModel
from services.db_services import DatabaseService
from services.search_service import SearchService

# MetadataService handles the metadata operations, including saving and searching metadata.
class MetadataService:
    def __init__(self):
        """
        :summary: Initialize the MetadataService with database and search services.
        """
        self.db_service = DatabaseService()
        self.search_service = SearchService()

    def ingest_metadata(self, asset_id:str, metadata: MetadataDBModel):
        """
        :summary: Save metadata to the database.
        :param: asset id of metadata
        :param metadata: The metadata object to save.
        :return: Asset id
        """
        self.transformations()
        status = self.db_service.save_metadata(asset_id, metadata)
        if status:
            # Optionally update search index
            self.search_service.index_metadata(metadata)
        return status

    def search_metadata(self, query: str, limit: int, offset: int):
        """
        :summary: Search for metadata using the search service.
        :param query: The search query string.
        """
        return self.search_service.search(query, limit, offset)

    def transformations(self):
        pass