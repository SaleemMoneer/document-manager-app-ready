FROM python:3.11-slim

RUN apt-get update && apt-get install -y     python3-tk     tk     libx11-6     && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY src/ /app/
RUN pip install firebase-admin
CMD ["python", "document_manager_app.py"]
