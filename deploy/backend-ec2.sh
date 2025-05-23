#!/bin/bash

# Install Docker
sudo apt update && sudo apt install -y docker.io
sudo usermod -aG docker $USER

# Pull code (or clone your repo)
git clone https://github.com/your/repo.git
cd repo

# Build and run application
docker build -t jobairo-app -f app/Dockerfile .
docker run -d \
  --env-file .env \
  -p 8000:8000 \
  --name app \
  jobairo-app
