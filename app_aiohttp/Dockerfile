FROM python:3.10-slim-bookworm

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir aiohttp==3.9.1

# Copy application
COPY aiohttp_app.py .

# Run app
EXPOSE 8080
CMD ["python", "aiohttp_app.py"]
