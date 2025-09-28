# Use official Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

# Install uv (fast dependency installer) or pip
RUN pip install --upgrade pip uv

COPY pyproject.toml uv.lock ./

RUN uv pip install . --system --no-cache


# Copy source code
COPY src ./src

# Expose port
EXPOSE 8000

# Run the app with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
