import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from services.search_service import SearchService
from models.validation import MetadataSearchResult

@pytest.fixture
def mock_data():
    return [
        MetadataSearchResult(
            asset_id="mysql_db1_users_tenant123",
            name="Users Table",
            type="table",
            source_type="MySQL",
            source_id="db1.users",
            metadata={"description": "User information"},
            tags=["sensitive", "user_data"],
            timestamp=datetime(2025, 4, 15),
            tenant_id="tenant123"
        ),
        MetadataSearchResult(
            asset_id="mysql_db1_orders_tenant123",
            name="Orders Table",
            type="table",
            source_type="MySQL",
            source_id="db1.orders",
            metadata={"description": "Order information"},
            tags=["sales", "order_data"],
            timestamp=datetime(2025, 4, 15),
            tenant_id="tenant123"
        ),
        MetadataSearchResult(
            asset_id="postgres_db2_products_tenant123",
            name="Products Database",
            type="database",
            source_type="PostgreSQL",
            source_id="db2.products",
            metadata={"description": "Product catalog"},
            tags=["catalog"],
            timestamp=datetime(2025, 4, 15),
            tenant_id="tenant123"
        ),
    ]

@pytest.fixture
def search_service(mock_data):
    service = SearchService()
    # Add the mock data directly to the instance, not to the class
    service._mock_data = mock_data
    return service

@pytest.mark.parametrize("query,limit,offset,expected_count,expected_names", [
    # Basic query matching two items
    ("Table", 10, 0, 2, ["Users Table", "Orders Table"]),
    # Specific table query
    ("Users", 10, 0, 1, ["Users Table"]),
    # Query matching an asset_id
    ("mysql_db1_users", 10, 0, 1, ["Users Table"]),
    # Query with pagination
    ("Table", 1, 0, 1, ["Users Table"]),
    ("Table", 1, 1, 1, ["Orders Table"]),
    # Query with no matches
    ("NonExistent", 10, 0, 0, []),
    # Empty query (matches everything)
    ("", 10, 0, 3, ["Users Table", "Orders Table", "Products Database"]),
    # Query matching by type
    ("database", 10, 0, 1, ["Products Database"]),
])
async def test_search(query, limit, offset, expected_count, expected_names, search_service):
    """Test search with various queries and parameters"""
    # Perform the search
    response = await search_service.search(query, limit, offset)
    
    # Verify the response
    assert len(response.results) == expected_count
    
    # Check that the expected names are present in the results
    result_names = [r.name for r in response.results]
    assert all(name in result_names for name in expected_names)
    
    # Verify correct pagination
    assert response.limit == limit
    assert response.offset == offset
    
    # Total should reflect the total matches before pagination
    if query == "Table":
        assert response.total == 2
    elif query == "NonExistent":
        assert response.total == 0
    elif query == "":
        assert response.total == 3