#!/bin/bash
set -e

echo "Stopping and removing the Docker container..."
docker-compose -f scripts/docker-compose.yml -p queuetopia down

IMAGE_NAME="queuetopia-account-manager"

echo "Removing Docker image: $IMAGE_NAME..."
docker rmi -f $IMAGE_NAME || echo "Image $IMAGE_NAME not found."

echo "Cleaning up unused Docker resources..."
docker system prune -af

echo "Checking running containers..."
docker ps -a
