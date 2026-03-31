from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from .config import settings

pwd = CryptContext(schemes=["bcrypt"])
def hash_pw(p): return pwd.hash(p)
def verify_pw(p, h): return pwd.verify(p, h)
def create_token(data: dict):
    data["exp"] = datetime.utcnow() + timedelta(days=7)
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
