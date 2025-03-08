from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import CompanyTable, StoreTable
from schemas import CreateStore, EditStore, EditStoreStatus


async def create_store(db: AsyncSession, store: CreateStore):
  db_store = StoreTable(
    name=store.name,
    alias=store.alias,
    company_id=store.company_id
  )
  db.add(db_store)
  await db.commit()
  await db.refresh(db_store)
  return db_store


async def get_stores_by_c_id(db: AsyncSession, c_id: int):
  """Retrieve a list of stores associated with a given c_id."""
  result = await db.execute(select(StoreTable).join(CompanyTable, StoreTable.company_id == CompanyTable.id)
  .filter(
    CompanyTable.c_id == c_id,
    CompanyTable.deactivated == False,
    StoreTable.deactivated == False)
  )
  return result.scalars().all()


async def get_store_by_id(db: AsyncSession, s_id: int):
  """Retrieve store details with a given s_id."""
  result = await db.execute(select(StoreTable).filter(StoreTable.s_id == s_id, StoreTable.deactivated == False))
  return result.scalar_one_or_none()


async def edit_store(db: AsyncSession, store: EditStore):
  """Edit the name and alias of a store by its ID."""
  result = await db.execute(select(StoreTable).filter(StoreTable.id == store.id))
  db_store = result.scalars().first()

  if db_store is None:
    return None

  db_store.name = store.name
  db_store.alias = store.alias

  await db.commit()
  await db.refresh(db_store)

  return db_store


async def edit_store_status(db: AsyncSession, store: EditStoreStatus):
  """Edit the status of a store by its ID."""
  result = await db.execute(select(StoreTable).filter(StoreTable.id == store.id))
  db_store = result.scalars().first()

  if db_store is None:
    return None

  db_store.deactivated = store.deactivated

  await db.commit()
  await db.refresh(db_store)

  return db_store
