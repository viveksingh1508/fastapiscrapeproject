#!/bin/bash

# Install Docker
sudo apt update && sudo apt install -y docker.io
sudo usermod -aG docker $USER

# Pull code
git clone https://github.com/your/repo.git
cd repo

# Build image (same for worker & beat)
docker build -t jobairo-scraper -f scraper/Dockerfile .

# Start worker
docker run -d \
  --env-file .env \
  --name celery-worker \
  jobairo-scraper \
  celery -A tasks worker --loglevel=info

# Start beat
docker run -d \
  --env-file .env \
  --name celery-beat \
  jobairo-scraper \
  celery -A tasks beat --loglevel=info
