from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from repository import company as crud
from db.database import get_db

router = APIRouter()


@router.post("/create")
async def create(company: schemas.CreateCompany, db: AsyncSession = Depends(get_db)):
  """Create a new company object"""
  try:
    new_company = await crud.create_company(db, company)
    if not new_company:
      raise HTTPException(status_code=400, detail="Failed to create company")
    return JSONResponse(
      status_code=201,
      content={"message": "Company created successfully", "id": new_company.id, "company": new_company.name}
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/get/{user_id}", response_model=list[schemas.CompanyResponse])
async def get_companies(user_id: str, db: AsyncSession = Depends(get_db)):
  """Retrieve a list of company objects for a specific user_id"""
  companies = await crud.get_companies_by_user_id(db, user_id)

  if not companies:
    raise HTTPException(status_code=404, detail="No companies found for this user")

  return companies


@router.get("/get/details/{c_id}", response_model=schemas.CompanyResponse)
async def get_profile(c_id: int, db: AsyncSession = Depends(get_db)):
  """Retrieve a single company object by c_id"""
  company = await crud.get_company_by_c_id(db, c_id)
  if not company:
    raise HTTPException(status_code=404, detail="Company not found")

  return company


@router.post("/edit")
async def edit_company(company: schemas.EditCompany, db: AsyncSession = Depends(get_db)):
  """Edit the name, uen, and email of a company by its ID"""
  updated_company = await crud.edit_company(db, company)

  if updated_company is None:
    raise HTTPException(status_code=404, detail="Company not found")

  return JSONResponse(
    status_code=200,
    content={"message": "Company updated successfully", "id": updated_company.id, "userId": updated_company.user_id}
  )


@router.post("/deactivate/{id}")
async def deactivate_company(id: str, db: AsyncSession = Depends(get_db)):
  """Set the status of a company by its ID"""
  updated_company = await crud.edit_company_status(db, schemas.EditCompanyStatus(id=id, deactivated=True))

  if updated_company is None:
    raise HTTPException(status_code=404, detail="Company not found")

  return JSONResponse(
    status_code=200,
    content={"message": "Company deactivated successfully", "id": updated_company.id, "userId": updated_company.user_id}
  )
