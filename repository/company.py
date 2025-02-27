from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas import CreateCompany, EditCompany, EditCompanyStatus
from db.models import CompanyTable


async def create_company(db: AsyncSession, company: CreateCompany):
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


async def edit_company(db: AsyncSession, company: EditCompany):
  """Edit the name, uen, and email of a company by its ID."""
  result = await db.execute(select(CompanyTable).filter(CompanyTable.id == company.id))
  db_company = result.scalars().first()

  if db_company is None:
    return None

  db_company.name = company.name
  db_company.uen = company.uen
  db_company.email = company.email

  await db.commit()
  await db.refresh(db_company)

  return db_company


async def edit_company_status(db: AsyncSession, company: EditCompanyStatus):
  """Edit the status of a company by its ID."""
  result = await db.execute(select(CompanyTable).filter(CompanyTable.id == company.id))
  db_company = result.scalars().first()

  if db_company is None:
    return None

  db_company.deactivated = company.deactivated

  await db.commit()
  await db.refresh(db_company)

  return db_company
