# services/db_service.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from config.config import Config
from models.metadata import MetadataDBModel

# DatabaseService handles the database connection and operations
class DatabaseService:
    def __init__(self):
        """
        :summary: Initialize the DatabaseService with a database session.
        """
        self.db_session = self._get_db_session()

    def _get_db_session(self):
        """
        :summary: Create a new database session.
        :return: A new database session.
        """
        DATABASE_URL = Config.DATABASE_URL
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal()

    def save_metadata(self, asset_id: str, metadata: MetadataDBModel) -> bool:
        """
        :summary: Save metadata to the database.
        :param asset_id: Asset id of metadata
        :param metadata: The metadata object to save.
        :return: True if saved successfully, False otherwise.
        :raises IntegrityError: If there is a database integrity error.
        """
        try:
            db_metadata = MetadataDBModel(
                asset_id=asset_id,
                name=metadata.metadata.name,  # Nested field
                type=metadata.type if hasattr(metadata, "type") else "unknown",  # Optional fallback
                source_type=metadata.source_type,
                source_id=metadata.source_id,
                metadata_json=metadata.metadata.dict(),  # Save full details
                tags=metadata.tags,
                timestamp=metadata.timestamp,
                tenant_id=metadata.tenant_id
            )

            self.db_session.add(db_metadata)
            self.db_session.commit()
            self.db_session.refresh(db_metadata)
            return True
        except IntegrityError:
            self.db_session.rollback()
            return False

    def close(self):
        """
        :summary: Close the database session.
        """
        self.db_session.close()
