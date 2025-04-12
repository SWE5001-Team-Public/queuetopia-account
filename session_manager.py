import time
import uuid
from typing import Optional, Dict, Any

from fastapi import Depends, HTTPException, Request
from fastapi.security import APIKeyHeader
from redis.asyncio import Redis

from db.valkey_client import get_valkey

# Constants
SESSION_EXPIRY = 3600  # 1 hour in seconds
SESSION_PREFIX = "session:"

# Header-based auth for protected endpoints
session_header = APIKeyHeader(name="X-Session-Token", auto_error=False)


async def create_session(valkey: Redis, email: str, user_id: str, user_data: Dict[str, Any]) -> str:
  """
  Create a new login session for a user

  Args:
      valkey: Redis client
      email: User's email address
      user_id: User's unique ID
      user_data: Additional user data to store

  Returns:
      session_token: The generated session token
  """
  # Generate a unique session token
  session_token = str(uuid.uuid4())
  now = int(time.time())

  # Create session data
  session_data = {
    "session_token": session_token,
    "user_id": user_id,
    "email": email,
    "created_at": now,
    "expires_at": now + SESSION_EXPIRY,
    **{f"user_{k}": str(v) for k, v in user_data.items()}  # Prefix user data keys and ensure string values
  }

  # Store two entries:
  # 1. Map session token to email for quick lookup
  await valkey.set(f"token:{session_token}", email, ex=SESSION_EXPIRY)

  # 2. Store full session data using email as key
  await valkey.hset(f"{SESSION_PREFIX}{email}", mapping=session_data)
  await valkey.expire(f"{SESSION_PREFIX}{email}", SESSION_EXPIRY)

  return session_token


async def verify_session(valkey: Redis, session_token: str) -> Optional[Dict[str, Any]]:
  """
  Verify if a session token is valid and return session data

  Args:
      valkey: Redis client
      session_token: The session token to verify

  Returns:
      Dict of session data or None if session is invalid
  """
  # Get email from token
  email = await valkey.get(f"token:{session_token}")
  if not email:
    return None

  # Get session data
  session_data = await valkey.hgetall(f"{SESSION_PREFIX}{email}")
  if not session_data:
    return None

  # Check if session has expired
  now = int(time.time())
  expires_at = int(session_data.get("expires_at", 0))

  if expires_at < now:
    # Clean up expired session
    await invalidate_session(valkey, email)
    return None

  # Return session data
  return session_data


async def invalidate_session(valkey: Redis, email: str) -> bool:
  """Invalidate a user session (logout)"""
  # Get session token
  session_data = await valkey.hgetall(f"{SESSION_PREFIX}{email}")
  if not session_data:
    return False

  session_token = session_data.get("session_token")

  # Delete both entries
  if session_token:
    await valkey.delete(f"token:{session_token}")

  await valkey.delete(f"{SESSION_PREFIX}{email}")
  return True


# FastAPI dependency for protected routes
async def get_current_user(
  request: Request,
  session_token: str = Depends(session_header),
  valkey: Redis = Depends(get_valkey)
) -> Dict[str, Any]:
  """Dependency to verify session and get current user info"""
  if not session_token:
    raise HTTPException(status_code=401, detail="Not authenticated")

  session_data = await verify_session(valkey, session_token)
  if not session_data:
    raise HTTPException(status_code=401, detail="Session expired or invalid")

  # Extract user data from session
  user_data = {
    "user_id": session_data.get("user_id"),
    "email": session_data.get("email"),
  }

  # Add any custom user data from session (prefixed with "user_")
  for key, value in session_data.items():
    if key.startswith("user_") and key != "user_id":
      user_data[key[5:]] = value  # Remove "user_" prefix

  return user_data
