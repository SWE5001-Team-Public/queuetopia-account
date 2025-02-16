from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from db import crud
from db.database import get_db

router = APIRouter()


@router.post("/create")
async def create(company: schemas.Company, db: AsyncSession = Depends(get_db)):
  new_company = await crud.create_company(db, company)
  return JSONResponse(
    status_code=201,
    content={"message": "Company created successfully", "company": new_company.name}
  )


@router.get("/get/{user_id}", response_model=list[schemas.Company])
async def get_companies(user_id: str, db: AsyncSession = Depends(get_db)):
  """Retrieve a list of company objects for a specific user_id"""
  companies = await crud.get_companies_by_user_id(db, user_id)

  if not companies:
    raise HTTPException(status_code=404, detail="No companies found for this user")

  return companies
