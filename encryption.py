from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
  try:
    return pwd_context.verify(plain_password, hashed_password)
  except Exception as e:
    print(f"Password verification error: {str(e)}")
    return False


def get_password_hash(password):
  return pwd_context.hash(password)
