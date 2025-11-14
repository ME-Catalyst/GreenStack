FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY bridge.py .

# Run the bridge service
CMD ["python", "-u", "bridge.py"]
