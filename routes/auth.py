import json
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from aws.sqs import send_message
from constants.Role import Role
from db.database import get_db
from db.valkey_client import get_valkey
from encryption import verify_password
from repository import account as crud
from session_manager import get_current_user, invalidate_session, create_session

router = APIRouter()


@router.post("/register")
async def register(user: schemas.User, db: AsyncSession = Depends(get_db)):
  existing_user = await crud.get_user_by_email(db, user.email)
  if existing_user:
    raise HTTPException(status_code=400, detail="User already exists")

  try:
    new_user = await crud.create_user(db, user, Role.BUSINESS_OWNER)

    if not new_user:
      raise HTTPException(status_code=400, detail="Failed to create user")

    user_data = {
      "first_name": user.first_name,
      "last_name": user.last_name,
      "email": user.email,
      "role": Role.BUSINESS_OWNER,
    }
    await send_message(json.dumps(user_data), "register-user-event", "register")

    return JSONResponse(
      status_code=201,
      content={"message": "User registered successfully", "user": new_user.email}
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post("/register/staff")
async def register_staff(staff: schemas.Staff, db: AsyncSession = Depends(get_db)):
  existing_user = await crud.get_user_by_email(db, staff.email)
  if existing_user:
    raise HTTPException(status_code=400, detail="User already exists")

  try:
    password = "temp-123"
    new_user = schemas.User(email=staff.email, first_name=staff.first_name, last_name=staff.last_name,
                            password=password)
    new_staff = await crud.create_user(db, new_user, Role.EMPLOYEE, c_id=staff.c_id)

    if not new_staff:
      raise HTTPException(status_code=400, detail="Failed to create user")

    user_data = {
      "first_name": staff.first_name,
      "last_name": staff.last_name,
      "email": staff.email,
      "password": password,
      "role": Role.EMPLOYEE,
    }
    await send_message(json.dumps(user_data), "register-user-event", "register")

    return JSONResponse(
      status_code=201,
      content={"message": "User created successfully", "user": new_staff.email}
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post("/login")
async def login(
  login_data: schemas.LoginRequest,
  db: AsyncSession = Depends(get_db),
  valkey: Redis = Depends(get_valkey)
):
  user = await crud.get_user_by_email(db, login_data.email)

  if user and verify_password(login_data.password, user.password):
    if user.email_confirmed is False:
      raise HTTPException(status_code=403, detail="Email not confirmed")

    # Create a session for the authenticated user
    user_data = {
      "first_name": user.first_name,
      "last_name": user.last_name,
      "email_confirmed": user.email_confirmed
    }

    # Create session and get token
    session_token = await create_session(valkey, user.email, str(user.id), user_data)

    return JSONResponse(
      status_code=200,
      content={
        "message": "Login successful",
        "user": user.email,
        "session_token": session_token
      },
      headers={"X-Session-Token": session_token}  # Also include in header for easy client usage
    )

  raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/logout")
async def logout(
  user_data: Dict[str, Any] = Depends(get_current_user),
  valkey: Redis = Depends(get_valkey)
):
  """Logout endpoint - invalidates the current session"""
  email = user_data.get("email")
  success = await invalidate_session(valkey, email)

  if not success:
    raise HTTPException(status_code=400, detail="Logout failed")

  return JSONResponse(
    content={"message": "Logged out successfully"},
    status_code=200
  )


@router.get("/session-check")
async def check_session(user_data: Dict[str, Any] = Depends(get_current_user)):
  """Simple endpoint to verify if a session is valid"""
  return JSONResponse(
    content={
      "message": "Session is valid",
      "email": user_data.get("email")
    },
    status_code=200
  )


@router.post("/confirm-email")
async def confirm_email(body: schemas.ConfirmEmailRequest, db: AsyncSession = Depends(get_db)):
  user = await crud.confirm_email(db, body.email)

  if not user:
    raise HTTPException(status_code=404, detail="Invalid request")

  return JSONResponse(
    status_code=200,
    content={"message": "Email confirmed successfully", "user": user.email}
  )


@router.post("/change-password")
async def change_password(body: schemas.ChangePasswordRequest, db: AsyncSession = Depends(get_db)):
  user = await crud.change_password(db, body)

  if not user:
    raise HTTPException(status_code=400, detail="Failed to change password")

  return JSONResponse(
    status_code=200,
    content={"message": "Password updated successfully", "user": user.email}
  )
