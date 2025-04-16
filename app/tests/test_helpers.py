import pytest
from utils.helpers import Helpers  # Adjust the import based on where your Helpers class is located

@pytest.mark.parametrize(
    "source_type, source_id, tenant_id, expected",
    [
        ("MySQL", "db1.users", "tenant_123", "tenan_mysql_db1.u_61fa2w0n"),  # Example expected value
        ("MySQL", "db1.users", "tenant_456", "tenan_mysql_db1.u_gzw66tf3"),
        ("PostgreSQL", "db2.products", "tenant_123", "tenan_postg_db2.p_yuvellw6"),
        ("MySQL", "db1.orders", "tenant_123", "tenan_mysql_db1.o_xwhltoy0"),
        ("My", "db", "tenant", "tenan_my_db_cyqam9wm"),  # Short strings edge case
        ("", "", "", "___mrh00rge"),  # Empty input edge case
    ]
)
def test_generate_unique_asset_id(source_type, source_id, tenant_id, expected):
    # Generate the result using the Helpers.generate method
    result = Helpers.generate(source_type, source_id, tenant_id)
    
    # Assert that the result matches the expected value
    assert result == expected, f"Expected {expected}, but got {result}"

