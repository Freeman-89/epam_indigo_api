FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt
COPY ./app .


FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libfreetype6 \
    libfontconfig1 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=builder /install /usr/local
COPY --from=builder /app /app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app", "--workers", "1", "--threads", "2"]

