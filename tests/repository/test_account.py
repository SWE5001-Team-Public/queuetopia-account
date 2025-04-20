import datetime
import uuid
from unittest.mock import patch, AsyncMock

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from constants.Role import Role
from db.base import Base
from db.models import UserTable
from repository.account import (
  create_user, get_user_by_email, get_user_by_email_ignore_status,
  get_accounts_by_c_id, confirm_email, change_password, change_status
)
from schemas import User, ChangePasswordRequest, ChangeStatusRequest

# Create test database engine (using SQLite in-memory for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(
  class_=AsyncSession,
  expire_on_commit=False,
  autocommit=False,
  autoflush=False,
  bind=engine,
)


@pytest_asyncio.fixture
async def db_session():
  """Create a clean database session for each test."""
  # Create tables
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  # Create session
  async with TestingSessionLocal() as session:
    yield session

  # Clean up after test
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_user():
  # Arrange
  mock_session = AsyncMock(spec=AsyncSession)

  # Set up the mock to capture the added user
  captured_user = None

  async def mock_add(user):
    nonlocal captured_user
    captured_user = user

  mock_session.add.side_effect = mock_add

  # Create test user data
  test_user = User(
    email="test@example.com",
    first_name="Test",
    last_name="User",
    password="password123"
  )

  # Mock password hashing
  with patch('repository.account.get_password_hash', return_value="hashed_password123"):
    # Act
    result = await create_user(mock_session, test_user, Role.CUSTOMER)

    # Assert
    # Verify session.add was called
    mock_session.add.assert_called_once()

    # Verify session.commit was called
    mock_session.commit.assert_called_once()

    # Verify the user was created with correct properties
    assert captured_user.email == "test@example.com"
    assert captured_user.first_name == "Test"
    assert captured_user.last_name == "User"
    assert captured_user.role == Role.CUSTOMER
    assert captured_user.password == "hashed_password123"
    assert captured_user.u_id is not None  # Ensure u_id was set
    assert not captured_user.deactivated  # Should default to False

    # Verify returned data matches what we expect
    assert result is not None
    assert result.email == "test@example.com"
    assert result.first_name == "Test"
    assert result.last_name == "User"
    assert result.role == Role.CUSTOMER
    assert result.password == "hashed_password123"


@pytest.mark.asyncio
async def test_get_user_by_email(db_session):
  # Arrange - Create a test user
  user_id = str(uuid.uuid4())
  test_user = UserTable(
    id=user_id,
    u_id=1,
    email="get_test@example.com",
    first_name="Get",
    last_name="Test",
    password="hashed_password",
    role=Role.BUSINESS_OWNER,
    created_at=datetime.datetime.now(),
    updated_at=datetime.datetime.now(),
    deactivated=False
  )
  db_session.add(test_user)
  await db_session.commit()

  # Act
  result = await get_user_by_email(db_session, "get_test@example.com")

  # Assert
  assert result is not None
  assert result.email == "get_test@example.com"
  assert result.id == user_id

  # Test with non-existent email
  result = await get_user_by_email(db_session, "nonexistent@example.com")
  assert result is None

  # Test with deactivated user
  test_user.deactivated = True
  await db_session.commit()
  result = await get_user_by_email(db_session, "get_test@example.com")
  assert result is None


@pytest.mark.asyncio
async def test_get_user_by_email_ignore_status(db_session):
  # Arrange - Create a test user
  user_id = str(uuid.uuid4())
  test_user = UserTable(
    id=user_id,
    u_id=1,
    email="ignore_status@example.com",
    first_name="Ignore",
    last_name="Status",
    password="hashed_password",
    role=Role.EMPLOYEE,
    created_at=datetime.datetime.now(),
    updated_at=datetime.datetime.now(),
    deactivated=True  # User is deactivated
  )
  db_session.add(test_user)
  await db_session.commit()

  # Act
  result = await get_user_by_email_ignore_status(db_session, "ignore_status@example.com")

  # Assert
  assert result is not None
  assert result.email == "ignore_status@example.com"
  assert result.deactivated is True


@pytest.mark.asyncio
async def test_get_accounts_by_c_id(db_session):
  # Arrange - Create multiple test users with the same company_id
  company_id = 1
  test_users = [
    UserTable(
      u_id=i + 1,  # Add u_id explicitly
      email=f"company_user{i}@example.com",
      first_name=f"Company{i}",
      last_name="User",
      password="hashed_password",
      role=Role.EMPLOYEE,
      company_id=company_id,
      created_at=datetime.datetime.now(),
      updated_at=datetime.datetime.now()
    ) for i in range(3)
  ]

  # Add a user with a different company_id
  different_company_user = UserTable(
    u_id=4,
    email="different@example.com",
    first_name="Different",
    last_name="Company",
    password="hashed_password",
    role=Role.EMPLOYEE,
    company_id=2,
    created_at=datetime.datetime.now(),
    updated_at=datetime.datetime.now()
  )

  db_session.add_all(test_users + [different_company_user])
  await db_session.commit()

  # Act
  result = await get_accounts_by_c_id(db_session, company_id)

  # Assert
  assert result is not None
  assert len(result) == 3
  emails = [user.email for user in result]
  assert "company_user0@example.com" in emails
  assert "company_user1@example.com" in emails
  assert "company_user2@example.com" in emails
  assert "different@example.com" not in emails


@pytest.mark.asyncio
async def test_confirm_email(db_session):
  # Arrange - Create a test user with unconfirmed email
  test_user = UserTable(
    u_id=1,
    email="unconfirmed@example.com",
    first_name="Unconfirmed",
    last_name="User",
    password="hashed_password",
    role=Role.CUSTOMER,
    email_confirmed=False,
    created_at=datetime.datetime.now(),
    updated_at=datetime.datetime.now()
  )
  db_session.add(test_user)
  await db_session.commit()

  # Act
  result = await confirm_email(db_session, "unconfirmed@example.com")

  # Assert
  assert result is not None
  assert result.email_confirmed is True
  assert result.confirmed_at is not None

  # Test confirming an already confirmed email
  result = await confirm_email(db_session, "unconfirmed@example.com")
  assert result is None

  # Test confirming a non-existent email
  result = await confirm_email(db_session, "nonexistent@example.com")
  assert result is None


@pytest.mark.asyncio
async def test_change_password(db_session):
  # Need to patch the verify_password and get_password_hash functions
  with patch('repository.account.verify_password', return_value=True), \
    patch('repository.account.get_password_hash', return_value="new_hashed_password"):
    # Arrange - Create a test user
    test_user = UserTable(
      u_id=1,
      email="password@example.com",
      first_name="Password",
      last_name="Change",
      password="old_hashed_password",
      role=Role.CUSTOMER,
      created_at=datetime.datetime.now(),
      updated_at=datetime.datetime.now()
    )
    db_session.add(test_user)
    await db_session.commit()

    old_updated_at = test_user.updated_at

    # Act
    request = ChangePasswordRequest(
      email="password@example.com",
      old_password="old_password",
      new_password="new_password"
    )
    result = await change_password(db_session, request)

    # Assert
    assert result is not None
    assert result.password == "new_hashed_password"
    assert result.updated_at > old_updated_at

    # Test with invalid old password
    with patch('repository.account.verify_password', return_value=False):
      result = await change_password(db_session, request)
      assert result is None


@pytest.mark.asyncio
async def test_change_status(db_session):
  # Arrange - Create a test user
  test_user = UserTable(
    u_id=1,
    email="status@example.com",
    first_name="Status",
    last_name="Change",
    password="hashed_password",
    role=Role.CUSTOMER,
    deactivated=False,
    created_at=datetime.datetime.now(),
    updated_at=datetime.datetime.now()
  )
  db_session.add(test_user)
  await db_session.commit()

  old_updated_at = test_user.updated_at

  # Act - Deactivate
  request = ChangeStatusRequest(
    email="status@example.com",
    deactivated=True
  )
  result = await change_status(db_session, request)

  # Assert
  assert result is not None
  assert result.deactivated is True
  assert result.updated_at > old_updated_at

  # Act - Reactivate
  request.deactivated = False
  old_updated_at = result.updated_at
  result = await change_status(db_session, request)

  # Assert
  assert result is not None
  assert result.deactivated is False
  assert result.updated_at > old_updated_at
