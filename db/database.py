import logging
import os
import ssl

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import load_environment, setup_logging
from constants.Role import Role
from db.base import Base
from db.models import RoleTable

load_environment()
setup_logging()

logger = logging.getLogger(__name__)

ENVIRONMENT = os.getenv("ENVIRONMENT", "prod")
DATABASE_URL = os.getenv("DATABASE_URL")

logger.info(f"🚀 Running in {ENVIRONMENT.upper()} environment")

# Ensure DATABASE_URL is set
if not DATABASE_URL:
  raise ValueError("DATABASE_URL is not set. Check your .env file.")

# Configure SSL context for production database (only if needed)
ssl_context = ssl.create_default_context() if ENVIRONMENT == "prod" else None

# Create async engine
engine = create_async_engine(
  DATABASE_URL,
  echo=True,
  connect_args={"ssl": ssl_context} if ssl_context else {}
)

SessionLocal = sessionmaker(
  autocommit=False,
  autoflush=False,
  class_=AsyncSession,
  expire_on_commit=False
)


# Function to create tables asynchronously
async def create_tables():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)


# Run table creation when the application starts
async def init_db():
  await create_tables()


# Insert static values
async def insert_static():
  async with SessionLocal(bind=engine) as session:
    try:
      records = [
        RoleTable(key=Role.ADMINISTRATOR, value='Administrator', hierarchy=0),
        RoleTable(key=Role.BUSINESS_OWNER, value='Business Owner', hierarchy=10),
        RoleTable(key=Role.EMPLOYEE, value='Employee', hierarchy=11),
        RoleTable(key=Role.CUSTOMER, value='Customer', hierarchy=99),
      ]
      session.add_all(records)
      await session.commit()
    except Exception as e:
      await session.rollback()
      logger.error(f"Error inserting records: {e}")


# Dependency for async DB session
async def get_db():
  async with SessionLocal(bind=engine) as session:
    yield session
