import os

import redis.asyncio as redis
from dotenv import load_dotenv

# Use the same environment loading logic as in database.py
ENVIRONMENT = os.getenv("ENVIRONMENT", "prod")

if ENVIRONMENT == "prod":
  load_dotenv(".env.production")
elif ENVIRONMENT == "local":
  load_dotenv(".env.local")
else:
  load_dotenv(".env")

# Configure Valkey connection parameters
VALKEY_HOST = os.getenv("VALKEY_HOST", "localhost")  # Use container name in Docker network
VALKEY_PORT = os.getenv("VALKEY_PORT", 6379)
VALKEY_PASSWORD = os.getenv("VALKEY_PASSWORD", "magical_password")
VALKEY_DB = os.getenv("VALKEY_DB", 0)

# Create a Redis connection pool
redis_pool = redis.ConnectionPool(
  host=VALKEY_HOST,
  port=int(VALKEY_PORT),
  password=VALKEY_PASSWORD,
  db=int(VALKEY_DB),
  decode_responses=True  # Automatically decode responses to Python strings
)


# Create a Redis client using the connection pool
async def get_valkey():
  client = redis.Redis.from_pool(redis_pool)
  try:
    yield client
  finally:
    await client.close()


# Utility functions for common operations
async def add_string(client, key, value, expiry_seconds=None):
  """Add a string value to Valkey"""
  await client.set(key, value, ex=expiry_seconds)


async def add_hash(client, key, mapping, expiry_seconds=None):
  """Add a hash (dictionary) to Valkey"""
  await client.hset(key, mapping=mapping)
  if expiry_seconds:
    await client.expire(key, expiry_seconds)


async def add_list(client, key, values, expiry_seconds=None):
  """Add values to a list in Valkey"""
  await client.rpush(key, *values)
  if expiry_seconds:
    await client.expire(key, expiry_seconds)
