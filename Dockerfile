# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers + OS dependencies
RUN playwright install --with-deps chromium firefox webkit

# Copy the rest of the project
COPY . .

# Create reports directory
RUN mkdir -p reports/screenshots reports/videos reports/traces

# Default command: run all tests
CMD ["pytest", "tests/", "-v", "--html=reports/report.html", "--self-contained-html"]
