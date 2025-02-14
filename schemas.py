import uuid

from pydantic import BaseModel


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
