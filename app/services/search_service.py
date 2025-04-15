from typing import List
from datetime import datetime
from models.validation import MetadataSearchResult, SearchResponse

class SearchService:
    def __init__(self):
        self._mock_data: List[MetadataSearchResult] = [
            MetadataSearchResult(
                asset_id="asset_001",
                name="Users Table",
                type="table",
                source_type="MySQL",
                source_id="db1.users",
                metadata={
                    "description": "User table",
                    "attributes": [{"name": "username", "type": "varchar"}]
                },
                tags=["user_data", "sensitive"],
                timestamp=datetime(2025, 4, 15, 12, 0, 0),
                tenant_id="tenant_123"
            ),
            MetadataSearchResult(
                asset_id="asset_002",
                name="JIRA Project Tracker",
                type="project",
                source_type="JIRA",
                source_id="jira.project123",
                metadata={
                    "description": "Tracks JIRA projects",
                    "attributes": [{"name": "project_key", "type": "string"}]
                },
                tags=["issue_tracking"],
                timestamp=datetime(2025, 4, 15, 13, 0, 0),
                tenant_id="tenant_123"
            ),
        ]

    def search(self, query: str, limit: int = 10, offset: int = 0) -> SearchResponse:
        # tenant isolation
        lowered_query = query.lower()
        filtered = (
            item for item in self._mock_data
            if lowered_query in item.asset_id.lower() or lowered_query in item.name.lower()
        )
        matched_items = list(filtered)
        paginated = matched_items[offset:offset + limit]

        print(f"[SearchServiceMock] Matched: {len(matched_items)}, Returning: {len(paginated)}")

        return SearchResponse(
            results=paginated,
            total=len(matched_items),
            limit=limit,
            offset=offset
        )
    
    def index_metadata(self, metadata):
        pass
