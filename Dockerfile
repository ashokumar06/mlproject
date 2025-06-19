# Multi-stage build optimized for ML/Data Science packages
FROM python:3.11-slim as builder

# Install system dependencies needed for building ML packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    gfortran \
    pkg-config \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies with optimizations for ML packages
RUN pip install --no-cache-dir --user \
    --compile \
    --global-option=build_ext \
    --global-option=-j4 \
    -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    awscli \
    curl \
    libopenblas0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && apt-get autoremove -y

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/app/.local

# Set working directory
WORKDIR /app

# Copy only essential application files
COPY --chown=app:app app.py .
COPY --chown=app:app requirements.txt .
# Add other necessary files individually instead of copying everything
# COPY --chown=app:app models/ ./models/
# COPY --chown=app:app data/ ./data/
# COPY --chown=app:app config/ ./config/

# Switch to non-root user
USER app

# Add local bin to PATH
ENV PATH=/home/app/.local/bin:$PATH

# Set environment variables for ML libraries
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV OMP_NUM_THREADS=1
ENV OPENBLAS_NUM_THREADS=1
ENV MKL_NUM_THREADS=1

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "app:app"]