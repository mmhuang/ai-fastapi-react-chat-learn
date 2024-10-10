from datetime import timedelta
from backend.utils import security
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from backend.schemas import UserSchema
from backend.models import User  # Add this line to import the User model

from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return security.get_current_user(token)

def validate_password(plain_password, hashed_password):
    return security.validate_password(plain_password, hashed_password)

def get_password_hash(password):
    return security.get_password_hash(password)

def create_access_token(data: dict, expires_delta=None):
    return security.create_access_token(data, expires_delta)

def validate_email_address(db: Session, email: str):
    return db.query(User).filter(User.email == email).first() is None

def get_password_hash(password):
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    from jose import JWTError, jwt
    from datetime import datetime
    SECRET_KEY = "YOUR_SECRET_KEY"
    ALGORITHM = "HS256"
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt