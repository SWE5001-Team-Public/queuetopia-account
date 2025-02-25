from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from db import crud
from db.database import get_db

router = APIRouter()


@router.post("/create")
async def create(store: schemas.Store, db: AsyncSession = Depends(get_db)):
  """Create a new store object"""
  new_store = await crud.create_store(db, store)
  return JSONResponse(
    status_code=201,
    content={"message": "Store created successfully", "id": new_store.id, "store": new_store.name}
  )


@router.get("/get/{c_id}", response_model=list[schemas.StoreResponse])
async def get_stores(c_id: int, db: AsyncSession = Depends(get_db)):
  """Retrieve a list of store objects for a specific c_id"""
  stores = await crud.get_stores_by_c_id(db, c_id)

  if not stores:
    raise HTTPException(status_code=404, detail="No stores found for this company")

  return stores
