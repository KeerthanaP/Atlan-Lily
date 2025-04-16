from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

# Base class for all SQLAlchemy models
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True  # This ensures BaseModel is not mapped to a table itself
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self, session):
        """ Save or update the current object in the database. """
        # tenant isolation
        session.add(self)
        session.commit()
        session.refresh(self)
    
    def delete(self, session):
        """ Delete the current object from the database. """
        # tenant isolation
        session.delete(self)
        session.commit()
