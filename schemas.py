import uuid

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
  user_id: str  # This is the user_id of the user who created the company

  class Config:
    alias_generator = to_camel
    populate_by_name = True  # Allows using both snake_case and camelCase
    from_attributes = True  # Needed for ORM models
