import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import UserTable
from encryption import get_password_hash
from schemas import User, LoginRequest, ChangeStatusRequest


async def create_user(db: AsyncSession, user: User, role: str, c_id: int = None):
  """Create a new user."""
  db_user = UserTable(
    email=user.email,
    first_name=user.first_name,
    last_name=user.last_name,
    role=role,
    company_id=c_id,
    password=get_password_hash(user.password),
    created_at=datetime.datetime.now(),
    updated_at=datetime.datetime.now(),
  )
  db.add(db_user)
  await db.commit()
  await db.refresh(db_user)
  return db_user


async def get_user_by_email(db: AsyncSession, email: str):
  """Retrieve a user by email."""
  result = await db.execute(select(UserTable).filter(UserTable.email == email, UserTable.deactivated == False))
  return result.scalar_one_or_none()


async def get_user_by_email_ignore_status(db: AsyncSession, email: str):
  """Retrieve a user by email."""
  result = await db.execute(select(UserTable).filter(UserTable.email == email))
  return result.scalar_one_or_none()


async def get_accounts_by_c_id(db: AsyncSession, c_id: int):
  """Retrieve a list of accounts associated with a given c_id."""
  result = await db.execute(select(UserTable).filter(UserTable.company_id == c_id))
  return result.scalars().all()


async def confirm_email(db: AsyncSession, email: str):
  """Confirm a user's email."""
  user = await get_user_by_email(db, email)

  if not user or user.email_confirmed:
    return None

  user.email_confirmed = True
  user.updated_at = datetime.datetime.now()
  user.confirmed_at = datetime.datetime.now()

  await db.commit()
  await db.refresh(user)
  return user


async def change_password(db: AsyncSession, req: LoginRequest):
  """Change a user's password."""
  user = await get_user_by_email(db, req.email)

  if not user or user.email_confirmed:
    return None

  user.password = get_password_hash(req.password)
  user.updated_at = datetime.datetime.now()

  await db.commit()
  await db.refresh(user)
  return user


async def change_status(db: AsyncSession, req: ChangeStatusRequest):
  """Change a user's status."""
  user = await get_user_by_email_ignore_status(db, req.email)

  user.deactivated = req.deactivated
  user.updated_at = datetime.datetime.now()

  await db.commit()
  await db.refresh(user)
  return user
