# main.py
from fastapi import FastAPI, Depends, HTTPException
from api.metadata import router as metadata_router
from services.auth_service import get_current_user

app = FastAPI()

# Include the metadata router for the relevant routes
app.include_router(metadata_router)

@app.get("/")
async def root():
    return {"message": "Atlan Lily Prototype Running!"}
