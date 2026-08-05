from datetime import datetime, timedelta
from typing import Optional, List
import jwt
from fastapi import HTTPException
import bcrypt
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from app.schemas.user import TokenData

SECRET_KEY = "sdfgsdfgsdfAIU123UIGSXQ230812"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    # Chuyển string thành bytes cho bcrypt
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password_byte_enc)

def get_password_hash(password):
    # Băm trực tiếp bằng bcrypt
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now()+ expires_delta
    else:
        expire = datetime.now() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not verify credentials",headers={"WWW-Authenticate": "Bearer"})
        return TokenData(username=username)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not verify credentials",headers={"WWW-Authenticate": "Bearer"})