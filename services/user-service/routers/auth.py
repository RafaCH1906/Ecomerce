from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from models.user import User
from services.auth import verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/login", summary="Iniciar sesión y obtener JWT", description="Retorna un token JWT compatible con products-service.")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Buscamos por nombre de usuario (o email)
    user = db.query(User).filter(User.nombre == form_data.username).first()
    if not user and "@" in form_data.username:
        user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Creamos la carga útil asegurando las variables esperadas por products-service (userId y sub)
    access_token = create_access_token(
        data={"sub": user.nombre, "userId": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}
