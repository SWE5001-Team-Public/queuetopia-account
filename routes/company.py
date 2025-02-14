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
