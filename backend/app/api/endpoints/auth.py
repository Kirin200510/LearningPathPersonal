from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import verify_password, create_access_token
from app.schemas.user import Token
from app.model.user import User  # Model SQLAlchemy của bạn
from datetime import timedelta
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/token/")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm=Depends(),
    db: Session = Depends(get_db),
) -> Token:
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong username or password"
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
