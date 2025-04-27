import logging
import os
import ssl
from datetime import datetime

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import load_environment, setup_logging
from constants.Role import Role
from db.base import Base
from db.models import RoleTable, UserTable, CompanyTable, StoreTable

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
  pool_pre_ping=True,
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


# Insert test data
async def insert_test_data():
  # Clean existing data first
  async with SessionLocal(bind=engine) as session:
    try:
      # Delete in reverse order to respect foreign key constraints
      await session.execute(delete(StoreTable))
      await session.execute(delete(CompanyTable))
      await session.execute(delete(UserTable))

      # Reset sequences
      await session.execute("ALTER SEQUENCE IF EXISTS store_s_id_seq RESTART WITH 1")
      await session.execute("ALTER SEQUENCE IF EXISTS company_c_id_seq RESTART WITH 1")
      await session.execute("ALTER SEQUENCE IF EXISTS user_u_id_seq RESTART WITH 1")

      await session.commit()
      logger.info("Cleaned existing test data and reset sequences")
    except Exception as e:
      await session.rollback()
      logger.error(f"Error cleaning existing data: {e}")

  # Step 1: Insert users
  async with SessionLocal(bind=engine) as session:
    try:
      users = [
        UserTable(
          id='11111111-1111-1111-1111-111111111111',
          email='owner1@example.com',
          first_name='John',
          last_name='Doe',
          password='$2b$12$WxbAh1mcZQuYL1vWUiEpTuN1qKtQaE2xdV5HMpjDvv2v6ZTW5I9v6',
          email_confirmed=True,
          role=Role.BUSINESS_OWNER,
          created_at=datetime.now(),
          updated_at=datetime.now(),
          confirmed_at=datetime.now()
        ),
        UserTable(
          id='22222222-2222-2222-2222-222222222222',
          email='owner2@example.com',
          first_name='Jane',
          last_name='Smith',
          password='$2b$12$WxbAh1mcZQuYL1vWUiEpTuN1qKtQaE2xdV5HMpjDvv2v6ZTW5I9v6',
          email_confirmed=True,
          role=Role.BUSINESS_OWNER,
          created_at=datetime.now(),
          updated_at=datetime.now(),
          confirmed_at=datetime.now()
        )
      ]
      session.add_all(users)
      await session.commit()
      logger.info("Successfully inserted test users")
    except Exception as e:
      await session.rollback()
      logger.error(f"Error inserting test users: {e}")
      return  # Exit if users can't be inserted

  # Step 2: Insert companies
  async with SessionLocal(bind=engine) as session:
    try:
      companies = [
        # Companies for owner1
        CompanyTable(
          id='aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
          name='Coffee Paradise',
          uen='T12345678A',
          email='coffee_paradise@example.com',
          user_id='11111111-1111-1111-1111-111111111111'
        ),
        CompanyTable(
          id='bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb',
          name='Sushi Bar',
          uen='T87654321B',
          email='sushi_bar@example.com',
          user_id='11111111-1111-1111-1111-111111111111'
        ),
        # Companies for owner2
        CompanyTable(
          id='cccccccc-cccc-cccc-cccc-cccccccccccc',
          name='WOW KBBQ',
          uen='T24681357C',
          email='wow_kbbq@example.com',
          user_id='22222222-2222-2222-2222-222222222222'
        ),
        CompanyTable(
          id='dddddddd-dddd-dddd-dddd-dddddddddddd',
          name='Gourmet Dining',
          uen='T13572468D',
          email='gourmet_dining@example.com',
          user_id='22222222-2222-2222-2222-222222222222'
        )
      ]
      session.add_all(companies)
      await session.commit()
      logger.info("Successfully inserted test companies")
    except Exception as e:
      await session.rollback()
      logger.error(f"Error inserting test companies: {e}")
      return  # Exit if companies can't be inserted

  # Step 3: Insert stores
  async with SessionLocal(bind=engine) as session:
    try:
      stores = [
        # Stores for Coffee Paradise
        StoreTable(
          id='eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee',
          name='Downtown Café',
          alias='CP',
          deactivated=False,
          company_id='aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        ),
        StoreTable(
          id='ffffffff-ffff-ffff-ffff-ffffffffffff',
          name='Riverside Coffee',
          alias='CP',
          deactivated=False,
          company_id='aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
        ),
        # Stores for Sushi Bar
        StoreTable(
          id='11111111-gggg-gggg-gggg-gggggggggggg',
          name='Ueno',
          alias='SB',
          deactivated=False,
          company_id='bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
        ),
        StoreTable(
          id='22222222-hhhh-hhhh-hhhh-hhhhhhhhhhhh',
          name='Nagoya',
          alias='SB',
          deactivated=False,
          company_id='bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
        ),
        # Stores for WOW KBBQ
        StoreTable(
          id='33333333-iiii-iiii-iiii-iiiiiiiiiiii',
          name='Yishun',
          alias='WK',
          deactivated=False,
          company_id='cccccccc-cccc-cccc-cccc-cccccccccccc'
        ),
        StoreTable(
          id='44444444-jjjj-jjjj-jjjj-jjjjjjjjjjjj',
          name='Bedok',
          alias='WK',
          deactivated=False,
          company_id='cccccccc-cccc-cccc-cccc-cccccccccccc'
        ),
        # Stores for Gourmet Dining
        StoreTable(
          id='55555555-kkkk-kkkk-kkkk-kkkkkkkkkkkk',
          name='Seaside Bistro',
          alias='GD',
          deactivated=False,
          company_id='dddddddd-dddd-dddd-dddd-dddddddddddd'
        ),
        StoreTable(
          id='66666666-llll-llll-llll-llllllllllll',
          name='Mountain View Restaurant',
          alias='GD',
          deactivated=False,
          company_id='dddddddd-dddd-dddd-dddd-dddddddddddd'
        )
      ]
      session.add_all(stores)
      await session.commit()
      logger.info("Successfully inserted test stores")
    except Exception as e:
      await session.rollback()
      logger.error(f"Error inserting test stores: {e}")

  logger.info("Test data insertion complete")


# Dependency for async DB session
async def get_db():
  async with SessionLocal(bind=engine) as session:
     yield session