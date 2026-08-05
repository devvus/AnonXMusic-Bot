FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including Node.js for yt-dlp JS support
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    gcc \
    libffi-dev \
    python3-dev \
    make \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "-m", "AnonXMusic"]
