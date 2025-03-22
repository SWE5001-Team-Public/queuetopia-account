import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from aws.sqs import send_message
from db.database import get_db
from repository import store as crud

router = APIRouter()


@router.post("/create")
async def create(store: schemas.CreateStore, db: AsyncSession = Depends(get_db)):
  """Create a new store object"""
  try:
    new_store = await crud.create_store(db, store)

    if not new_store:
      raise HTTPException(status_code=400, detail="Failed to create store")

    store_data = {
      "id": new_store.id,
      "s_id": new_store.s_id,
      "name": new_store.name,
      "alias": new_store.alias,
      "company_id": new_store.company_id,
    }
    await send_message(json.dumps(store_data), "store-create-event")

    return JSONResponse(
      status_code=201,
      content={"message": "Store created successfully", "id": new_store.id, "store": new_store.name}
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/get/{c_id}", response_model=list[schemas.StoreResponse])
async def get_stores(c_id: int, db: AsyncSession = Depends(get_db)):
  """Retrieve a list of store objects for a specific c_id"""
  stores = await crud.get_stores_by_c_id(db, c_id)

  if not stores:
    raise HTTPException(status_code=404, detail="No stores found for this company")

  return stores


@router.get("/details/{s_id}", response_model=schemas.StoreResponse)
async def get_store_by_id(s_id: int, db: AsyncSession = Depends(get_db)):
  """Retrieve store details by s_id"""
  store = await crud.get_store_by_id(db, s_id)

  if not store:
    raise HTTPException(status_code=404, detail="Store not found")

  return store


@router.get("/id/{id}", response_model=schemas.StoreResponse)
async def get_store_by_id(id: str, db: AsyncSession = Depends(get_db)):
  """Retrieve store details by id"""
  store = await crud.get_store_by_uuid(db, id)

  if not store:
    raise HTTPException(status_code=404, detail="Store not found")

  return store


@router.post("/edit")
async def edit_store(store: schemas.EditStore, db: AsyncSession = Depends(get_db)):
  """Edit the name and alias of a store by its ID"""
  updated_store = await crud.edit_store(db, store)

  if updated_store is None:
    raise HTTPException(status_code=404, detail="Store not found")

  store_data = {
    "id": updated_store.id,
    "name": updated_store.name,
    "alias": updated_store.alias,
  }
  await send_message(json.dumps(store_data), "store-update-event")

  return JSONResponse(
    status_code=200,
    content={"message": "Store updated successfully", "id": updated_store.id, "companyId": updated_store.company_id}
  )


@router.post("/deactivate/{id}")
async def deactivate_store(id: str, db: AsyncSession = Depends(get_db)):
  """Set the status of a store by its ID"""
  updated_store = await crud.edit_store_status(db, schemas.EditStoreStatus(id=id, deactivated=True))

  if updated_store is None:
    raise HTTPException(status_code=404, detail="Store not found")

  store_data = {
    "id": updated_store.id,
    "deactivated": updated_store.deactivated
  }
  await send_message(json.dumps(store_data), "store-deactivate-event")

  return JSONResponse(
    status_code=200,
    content={"message": "Store deactivated successfully", "id": updated_store.id, "companyId": updated_store.company_id}
  )
