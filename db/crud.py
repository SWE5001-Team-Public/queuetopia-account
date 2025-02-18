from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import schemas
from db import models


async def create_user(db: AsyncSession, user: schemas.User):
  db_user = models.UserTable(
    email=user.email,
    first_name=user.first_name,
    last_name=user.last_name,
    password=user.password
  )
  db.add(db_user)
  await db.commit()
  await db.refresh(db_user)
  return db_user


async def create_company(db: AsyncSession, company: schemas.Company):
  db_company = models.CompanyTable(
    name=company.name,
    uen=company.uen,
    email=company.email,
    user_id=company.user_id
  )
  db.add(db_company)
  await db.commit()
  await db.refresh(db_company)
  return db_company


async def create_store(db: AsyncSession, store: schemas.Store):
  db_store = models.StoreTable(
    name=store.name,
    alias=store.alias,
    company_id=store.company_id
  )
  db.add(db_store)
  await db.commit()
  await db.refresh(db_store)
  return db_store


async def get_user_by_email(db: AsyncSession, email: str):
  """Retrieve a user by email."""
  result = await db.execute(select(models.UserTable).filter(models.UserTable.email == email))
  return result.scalar_one_or_none()


async def get_companies_by_user_id(db: AsyncSession, user_id: str):
  """Retrieve a list of companies associated with a given user_id."""
  result = await db.execute(select(models.CompanyTable).filter(models.CompanyTable.user_id == user_id))
  return result.scalars().all()


async def get_company_by_c_id(db: AsyncSession, c_id: int):
  """Retrieve a company by c_id."""
  result = await db.execute(select(models.CompanyTable).filter(models.CompanyTable.c_id == c_id))
  return result.scalar_one_or_none()
