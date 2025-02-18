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
