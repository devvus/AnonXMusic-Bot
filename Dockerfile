FROM python:3.10-slim-buster

WORKDIR /app

# Install system dependencies for PyTgCalls
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    gcc \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "-m", "AnonXMusic"]
