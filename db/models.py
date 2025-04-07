import datetime
import uuid

from sqlalchemy import Column, String, ForeignKey, Integer, Sequence, Boolean, DateTime
from sqlalchemy.ext.hybrid import hybrid_property

from db.database import Base


class UserTable(Base):
  __tablename__ = "users"

  id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
  u_id = Column(Integer, Sequence('user_u_id_seq'), index=True, autoincrement=True, nullable=False)
  email = Column(String, unique=True, index=True, nullable=False)
  first_name = Column(String, nullable=False)
  last_name = Column(String, nullable=False)
  password = Column(String, nullable=False)
  email_confirmed = Column(Boolean, default=False)
  deactivated = Column(Boolean, default=False)
  created_at = Column(DateTime, default=datetime.datetime.now(), nullable=False)
  updated_at = Column(DateTime, default=datetime.datetime.now(), nullable=False)
  confirmed_at = Column(DateTime, default=None, nullable=True)

  @hybrid_property
  def display_id(self):
    return f"U{self.u_id}"


class CompanyTable(Base):
  __tablename__ = "companies"

  id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
  c_id = Column(Integer, Sequence('company_c_id_seq'), index=True, autoincrement=True, nullable=False)
  name = Column(String, nullable=False)
  uen = Column(String, nullable=False)
  email = Column(String, nullable=False)
  deactivated = Column(Boolean, default=False)
  user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

  @hybrid_property
  def display_id(self):
    return f"C{self.c_id}"


class StoreTable(Base):
  __tablename__ = "stores"

  id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
  s_id = Column(Integer, Sequence('store_s_id_seq'), index=True, autoincrement=True, nullable=False)
  name = Column(String, nullable=False)
  alias = Column(String, nullable=True)
  deactivated = Column(Boolean, default=False)
  company_id = Column(String, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

  @hybrid_property
  def display_id(self):
    return f"S{self.s_id}"
