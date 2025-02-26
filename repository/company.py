from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas import Company
from db.models import CompanyTable


async def create_company(db: AsyncSession, company: Company):
  db_company = CompanyTable(
    name=company.name,
    uen=company.uen,
    email=company.email,
    user_id=company.user_id
  )
  db.add(db_company)
  await db.commit()
  await db.refresh(db_company)
  return db_company


async def get_companies_by_user_id(db: AsyncSession, user_id: str):
  """Retrieve a list of companies associated with a given user_id."""
  result = await db.execute(
    select(CompanyTable).filter(CompanyTable.user_id == user_id, CompanyTable.deactivated == False))
  return result.scalars().all()


async def get_company_by_c_id(db: AsyncSession, c_id: int):
  """Retrieve a company by c_id."""
  result = await db.execute(select(CompanyTable).filter(CompanyTable.c_id == c_id, CompanyTable.deactivated == False))
  return result.scalar_one_or_none()
