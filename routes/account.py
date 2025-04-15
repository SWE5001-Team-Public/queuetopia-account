from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from db.database import get_db
from repository import account as crud

router = APIRouter()


@router.get("/profile/{email}")
async def get_profile(email: str, db: AsyncSession = Depends(get_db)):
  user = await crud.get_user_by_email(db, email)
  if not user:
    raise HTTPException(status_code=404, detail="User not found")

  return JSONResponse(
    status_code=200,
    content={"id": user.id, "email": user.email, "first_name": user.first_name, "last_name": user.last_name}
  )


@router.get("/get/{c_id}", response_model=list[schemas.StaffResponse])
async def get_stores(c_id: int, db: AsyncSession = Depends(get_db)):
  """Retrieve a list of account objects for a specific c_id"""
  stores = await crud.get_accounts_by_c_id(db, c_id)

  if not stores:
    raise HTTPException(status_code=404, detail="No accounts found for this company")

  return stores


@router.post("/edit/status")
async def edit_staff_status(staff: schemas.ChangeStatusRequest, db: AsyncSession = Depends(get_db)):
  updated_staff = await crud.change_status(db, staff)

  if updated_staff is None:
    raise HTTPException(status_code=404, detail="Staff details not found")

  return JSONResponse(
    status_code=200,
    content={"message": "Staff status updated successfully", "id": updated_staff.id,
             "companyId": updated_staff.company_id}
  )
