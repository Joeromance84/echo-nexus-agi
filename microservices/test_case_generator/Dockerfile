FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for AI extension
RUN useradd --create-home --shell /bin/bash agi-extension
RUN chown -R agi-extension:agi-extension /app
USER agi-extension

# Expose port
EXPOSE 8080

# Health check for AI extension
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Add AI extension metadata
LABEL ai.type="agi_extension" \
      ai.creator="market-analytics-orchestrator" \
      ai.capability="test_case_generation" \
      ai.version="1.0.0"

# Run the AI extension
CMD ["python", "main.py"]