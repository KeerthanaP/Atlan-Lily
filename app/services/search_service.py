# services/search_service.py
from typing import List
from models.metadata import Metadata

class SearchService:
    def index_metadata(self, metadata: Metadata):
        # Here you'd put logic to index metadata in Elasticsearch or another search engine
        pass

    def search(self, query: str, limit: int, offset: int) -> List[Metadata]:
        # Mocked search logic (can be replaced with actual search logic)
        return [{"asset_id": "db1.table1", "name": "Users", "type": "table"}]  # Mock response
