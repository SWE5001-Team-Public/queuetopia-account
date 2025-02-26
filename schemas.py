from pydantic import BaseModel
from humps import camelize


def to_camel(string: str) -> str:
  return camelize(string)


class User(BaseModel):
  email: str
  first_name: str
  last_name: str
  password: str


class LoginRequest(BaseModel):
  email: str
  password: str


class Company(BaseModel):
  name: str
  uen: str
  email: str
  user_id: str  # This is the id of the user who created the company


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
