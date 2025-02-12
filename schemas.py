from pydantic import BaseModel


class User(BaseModel):
  email: str
  first_name: str
  last_name: str
  password: str


class LoginRequest(BaseModel):
  email: str
  password: str
