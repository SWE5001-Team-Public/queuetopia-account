import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from aws.sqs import send_message
from db.database import get_db
from repository import account as crud

router = APIRouter()


@router.post("/register")
async def register(user: schemas.User, db: AsyncSession = Depends(get_db)):
  existing_user = await crud.get_user_by_email(db, user.email)
  if existing_user:
    raise HTTPException(status_code=400, detail="User already exists")

  try:
    new_user = await crud.create_user(db, user)

    if not new_user:
      raise HTTPException(status_code=400, detail="Failed to create user")

    user_data = {
      "first_name": user.first_name,
      "last_name": user.last_name,
      "email": user.email,
    }
    await send_message(json.dumps(user_data), "register-user-event", "register")

    return JSONResponse(
      status_code=201,
      content={"message": "User registered successfully", "user": new_user.email}
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post("/login")
async def login(login_data: schemas.LoginRequest, db: AsyncSession = Depends(get_db)):
  user = await crud.get_user_by_email(db, login_data.email)
  if user and user.password == login_data.password:
    return JSONResponse(
      status_code=200,
      content={"message": "Login successful", "user": user.email}
    )
  raise HTTPException(status_code=401, detail="Invalid credentials")
