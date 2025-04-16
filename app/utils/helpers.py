import hashlib
import base64

class Helpers:
    @staticmethod
    def generate(source_type: str, source_id: str, tenant_id: str) -> str:
        """
        Generate a unique asset_id by hashing tenant_id, source_type, and source_id.
        The result is base64 encoded for readability, and includes components of the input.
        The same asset_id will be generated for the same input every time.
        """
        unique_string = f"{tenant_id}_{source_type}_{source_id}"
        hash_object = hashlib.sha256(unique_string.encode())
        base64_hash = base64.urlsafe_b64encode(hash_object.digest()).decode('utf-8')
        readable_asset_id = f"{tenant_id[:5]}_{source_type[:5]}_{source_id[:5]}_{base64_hash[:8]}"
        return readable_asset_id.lower()
