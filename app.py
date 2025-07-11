import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from config import load_environment
from db.database import init_db, insert_static, insert_test_data
from routes import account, auth, company, store

load_dotenv()
load_environment()

ENVIRONMENT = os.getenv("ENVIRONMENT", "prod")


@asynccontextmanager
async def lifespan(app: FastAPI):
  """Initialize the database at startup."""
  await init_db()
  await insert_static()

  if ENVIRONMENT == "local":
    await insert_test_data()

  yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

router = APIRouter(prefix="/account-mgr")


# Health check endpoint
@router.get("/health", tags=["System"])
async def health_check():
  """Health check endpoint for monitoring service status."""
  return {"status": "healthy"}


# Other routes
router.include_router(auth.router, tags=["Authentication"])
router.include_router(account.router, prefix="/account", tags=["Account"])
router.include_router(company.router, prefix="/company", tags=["Company"])
router.include_router(store.router, prefix="/store", tags=["Store"])

app.include_router(router)

if __name__ == "__main__":
  uvicorn.run("app:app", host="0.0.0.0", port=5005)
