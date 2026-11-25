
# Start with a lightweight Python image
FROM python:3.14-slim

# Set the working directory inside the container
WORKDIR /app

# Prevent Python from buffering log output
ENV PYTHONUNBUFFERED=1

# Copy dependency definitions
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application files into the container
COPY . .

# Create directories required by the ETL pipeline
RUN mkdir -p /app/data/processed /app/logs

# Execute the ETL pipeline
CMD ["python", "src/pipeline/etl.py"]
