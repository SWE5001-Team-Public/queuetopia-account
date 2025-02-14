from sqlalchemy import Column, String, ForeignKey
import uuid

from db.database import Base


class UserTable(Base):
  __tablename__ = "users"

  id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
  email = Column(String, unique=True, index=True, nullable=False)
  first_name = Column(String, nullable=False)
  last_name = Column(String, nullable=False)
  password = Column(String, nullable=False)


class CompanyTable(Base):
  __tablename__ = "companies"

  id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
  name = Column(String, nullable=False)
  uen = Column(String, nullable=False)
  email = Column(String, nullable=False)
  user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
