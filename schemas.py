from datetime import datetime

from humps import camelize
from pydantic import BaseModel


def to_camel(string: str) -> str:
  return camelize(string)


class User(BaseModel):
  email: str
  first_name: str
  last_name: str
  password: str


class Staff(BaseModel):
  email: str
  first_name: str
  last_name: str
  c_id: int


class StaffResponse(BaseModel):
  id: str
  u_id: int
  email: str
  first_name: str
  last_name: str
  display_id: str
  role: str
  email_confirmed: bool
  deactivated: bool
  company_id: int | None
  created_at: datetime
  updated_at: datetime
  confirmed_at: datetime | None

  class Config:
    alias_generator = to_camel
    populate_by_name = True  # Allows using both snake_case and camelCase
    from_attributes = True  # Needed for ORM models


class LoginRequest(BaseModel):
  email: str
  password: str


class ChangePasswordRequest(BaseModel):
  email: str
  old_password: str
  new_password: str


class ChangeStatusRequest(BaseModel):
  email: str
  deactivated: bool


class ConfirmEmailRequest(BaseModel):
  email: str


class CreateCompany(BaseModel):
  name: str
  uen: str
  email: str
  user_id: str  # This is the id of the user who created the company


class EditCompany(BaseModel):
  id: str
  name: str
  uen: str
  email: str


class EditCompanyStatus(BaseModel):
  id: str
  deactivated: bool


class CompanyResponse(BaseModel):
  id: str
  c_id: int
  name: str
  uen: str
  email: str
  user_id: str  # This is the id of the user who created the company
  display_id: str

  class Config:
    alias_generator = to_camel
    populate_by_name = True  # Allows using both snake_case and camelCase
    from_attributes = True  # Needed for ORM models


class CreateStore(BaseModel):
  name: str
  alias: str | None
  company_id: str  # This is the id of the company that owns the store


class EditStore(BaseModel):
  id: str
  name: str
  alias: str | None


class EditStoreStatus(BaseModel):
  id: str
  deactivated: bool


class StoreResponse(BaseModel):
  id: str
  s_id: int
  name: str
  alias: str | None
  company_id: str  # This is the id of the company that owns the store
  display_id: str

  class Config:
    alias_generator = to_camel
    populate_by_name = True  # Allows using both snake_case and camelCase
    from_attributes = True  # Needed for ORM models
