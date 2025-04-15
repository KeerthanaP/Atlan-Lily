# services/db_service.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models.metadata import MetadataDB
from config.config import Config
from typing import Optional
from models.metadata import Metadata

# DatabaseService handles the database connection and operations
class DatabaseService:
    def __init__(self):
        """
        @summary: Initialize the DatabaseService with a database session.
        """
        self.db_session = self._get_db_session()

    def _get_db_session(self):
        """
        @summary: Create a new database session.
        @return: A new database session.
        """
        DATABASE_URL = Config.DATABASE_URL
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal()

    def save_metadata(self, metadata: Metadata) -> bool:
        """
        @summary: Save metadata to the database.
        @param metadata: The metadata object to save.
        @return: True if saved successfully, False otherwise.
        @raises IntegrityError: If there is a database integrity error.
        """
        try:
            db_metadata = MetadataDB(
                asset_id=metadata.asset_id,
                name=metadata.name,
                type=metadata.type,
                description=metadata.description,
                tags=metadata.tags,
                timestamp=metadata.timestamp,
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
        @summary: Close the database session.
        """
        self.db_session.close()
