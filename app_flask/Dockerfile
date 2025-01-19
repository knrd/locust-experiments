FROM python:3.10-slim-bookworm

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask==2.3.3

# Copy application
COPY flask_app.py .

# Run app
EXPOSE 5000
CMD ["python", "flask_app.py"]
