from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # Change this to restrict origins in production
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


# Health check endpoint for AWS ALB
@app.get("/health")
def health_check():
  return {"status": "healthy"}


# Pydantic model for user registration & login
class User(BaseModel):
  email: str
  first_name: str
  last_name: str
  password: str


class LoginRequest(BaseModel):
  email: str
  password: str


# Temporary in-memory user store for POC purposes
users: Dict[str, User] = {}


@app.post("/register")
def register(user: User):
  if user.email in users:
    return JSONResponse(
      status_code=400,
      content={"error": "User already exists", "email": user.email}
    )

  users[user.email] = user
  return JSONResponse(
    status_code=201,
    content={"message": "User registered successfully", "user": user.email}
  )


@app.post("/login")
def login(login_data: LoginRequest):
  user = users.get(login_data.email)

  if user and user.password == login_data.password:
    return JSONResponse(
      status_code=200,
      content={"message": "Login successful", "user": user.email}
    )

  return JSONResponse(
    status_code=401,
    content={"error": "Invalid credentials", "email": login_data.email}
  )


# Run the app using Uvicorn
if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="0.0.0.0", port=5000)
