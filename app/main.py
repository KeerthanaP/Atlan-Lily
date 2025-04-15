# main.py
from fastapi import FastAPI, Depends, HTTPException
from api.metadata import router as metadata_router
from api.auth import router as auth_router
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base
from config.config import Config

engine = create_engine(Config.DATABASE_URL)

# drop and clear db for testing purpose
# Base.metadata.drop_all(bind=engine)

# Create tables in the database (this only creates tables that don't already exist)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the metadata router for the relevant routes
app.include_router(metadata_router)

# Include the authentication routes
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Atlan Lily Prototype Running!"}
