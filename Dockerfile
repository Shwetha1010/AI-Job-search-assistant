FROM python:3.11-slim

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements-backend.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-backend.txt && \
    python -m spacy download en_core_web_sm

# Copy all application code
COPY . .

# HuggingFace Spaces uses port 7860
EXPOSE 7860

# Start FastAPI backend
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
