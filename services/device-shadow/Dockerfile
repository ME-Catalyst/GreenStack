FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY shadow_service.py .

# Run the shadow service
CMD ["python", "-u", "shadow_service.py"]
