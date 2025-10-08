FROM ubuntu:24.04

# Set working directory
WORKDIR /app

# Update package lists and install Python 3.12, pip, venv, and system dependencies
RUN apt-get update && \
    apt-get install -y python3.12 python3-pip python3.12-venv gcc ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /app/venv

# Activate virtual environment and upgrade pip
RUN /app/venv/bin/pip install --upgrade pip

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies in virtual environment
RUN /app/venv/bin/pip install -r requirements.txt

# Copy application files
COPY /app/ .

# Create a non-root user
# RUN useradd -m -u 1000 ctfuser && chown -R ctfuser:ctfuser /app
# USER ctfuser

# Expose port
EXPOSE 5000

# Set entrypoint to handle command line arguments using virtual environment python
ENTRYPOINT ["/app/venv/bin/python", "backend_server.py"]
