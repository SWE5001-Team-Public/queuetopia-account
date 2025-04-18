import random
import string

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


def generate_random_password(length=12):
  """
  Generate a random password with letters, numbers, and symbols.

  Args:
      length: Length of the password (default: 12)

  Returns:
      A random password string
  """
  # Character sets
  lowercase = string.ascii_lowercase
  uppercase = string.ascii_uppercase
  digits = string.digits
  symbols = "!@#$%^&*-_=+?"

  # Ensure at least one of each type
  password = [
    random.choice(lowercase),
    random.choice(uppercase),
    random.choice(digits),
    random.choice(symbols)
  ]

  # Fill the rest of the password
  remaining_length = length - 4
  all_chars = lowercase + uppercase + digits + symbols
  password.extend(random.choice(all_chars) for _ in range(remaining_length))

  # Shuffle to ensure the required characters aren't always at the beginning
  random.shuffle(password)

  return ''.join(password)
