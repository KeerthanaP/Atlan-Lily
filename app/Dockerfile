# Stage 1: Build Stage (Install dependencies)
FROM python:3.9-slim AS build

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Stage 2: Final Stage (Copy files and set up environment)
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Copy the installed dependencies from build stage
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

COPY --from=build /usr/local/bin /usr/local/bin

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Run FastAPI using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
