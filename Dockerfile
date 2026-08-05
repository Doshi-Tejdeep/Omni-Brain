FROM python:3.12-slim

LABEL maintainer="OmniBrain Team"
LABEL description="QA and testing container for OmniBrain"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements-dev.txt

COPY . .

CMD ["pytest"]
