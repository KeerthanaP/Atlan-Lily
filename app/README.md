# Atlan Lily Prototype

Prototype for metadata ingestion and retrieval.

### Features:
- **POST /metadata**: Ingest metadata with JSON schema validation.
- **GET /metadata/{asset_id}**: Retrieve metadata by asset ID.
- **Security**: JWT authentication for all endpoints.
- **Tech Stack**: Python FastAPI, Docker, pytest, JWT.

### Run Command:
To start the application using Docker Compose, run the following command:

```bash
docker-compose up --build

