FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY env/ ./env/

# Create output directories
RUN mkdir -p output/images output/videos output/audio src/logs

EXPOSE 5000

CMD ["python", "src/server/app.py"]
