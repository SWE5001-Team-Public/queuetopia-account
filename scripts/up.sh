#!/bin/bash
set -e

# Move to the project root (where Dockerfile is located)
cd "$(dirname "$0")/.." || exit

echo "Building the Docker image..."
docker build -t account-manager .

echo "Starting the Docker container..."
docker-compose -f scripts/docker-compose.yml -p queuetopia up -d --build

echo "Checking running containers..."
docker ps
