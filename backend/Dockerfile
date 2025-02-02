FROM python:3.7.11-slim

RUN apt-get update && \
    apt-get install -y \
    gdal-bin \
    libgdal-dev \
    build-essential \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/
RUN python3 -m venv /app/venv
RUN /app/venv/bin/python3 -m pip install --upgrade pip
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt --timeout 120

COPY sentinel5plib/google_credentials/credentials /root/.config/earthengine/credentials
RUN chmod 600 /root/.config/earthengine/credentials

COPY . /app/
ENV PATH="/app/venv/bin:$PATH"
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
