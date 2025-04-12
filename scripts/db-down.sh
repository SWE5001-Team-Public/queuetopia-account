#!/bin/bash
set -e

DB_CONTAINER="account-mgr-db"
VK_CONTAINER="account-mgr-vk"
DB_IMAGE="queuetopia-account-mgr-db"
VK_IMAGE="queuetopia-account-mgr-vk"
COMPOSE_FILE="scripts/docker-compose-db.yml"
VOLUME_NAME="queuetopia_account_postgres_data"

echo "Stopping and removing the PostgreSQL container..."
if command -v docker-compose &> /dev/null; then
    docker-compose -f "$COMPOSE_FILE" down -v
else
    docker compose -f "$COMPOSE_FILE" down -v
fi

# Stop and remove the database container if it exists
FOUND_CONTAINER=$(docker ps -a --format '{{.Names}}' | grep "^$DB_CONTAINER$" || true)

if [[ -n "$FOUND_CONTAINER" ]]; then
    echo "Stopping and removing database container: $DB_CONTAINER & $VK_CONTAINER..."
    docker stop "$DB_CONTAINER"
    docker rm "$DB_CONTAINER"
    echo "✅ Removed container: $DB_CONTAINER"
    docker stop "$VK_CONTAINER"
    docker rm "$VK_CONTAINER"
    echo "✅ Removed container: $VK_CONTAINER"
else
    echo "⚠️ Database container $DB_CONTAINER OR $VK_CONTAINER not found."
fi

# Remove the PostgreSQL image if it exists
if [[ -n $(docker images -q "$DB_IMAGE") ]]; then
    docker rmi -f "$DB_IMAGE"
    echo "✅ Removed image: $DB_IMAGE"
else
    echo "⚠️ Image $DB_IMAGE not found."
fi

# Remove the Valkey image if it exists
if [[ -n $(docker images -q "$VK_IMAGE") ]]; then
    docker rmi -f "$VK_IMAGE"
    echo "✅ Removed image: $VK_IMAGE"
else
    echo "⚠️ Image $VK_IMAGE not found."
fi

echo "Cleaning up unused Docker resources..."
docker image prune -af --filter "label=project=queuetopia-account-mgr" || echo "No unused images to remove."

# Remove the volume only if it exists
if docker volume inspect "$VOLUME_NAME" > /dev/null 2>&1; then
    docker volume rm "$VOLUME_NAME"
    echo "✅ Removed volume: $VOLUME_NAME"
else
    echo "⚠️ Volume $VOLUME_NAME not found or already removed."
fi

echo "✅ PostgreSQL container, image, and volume removed!"
