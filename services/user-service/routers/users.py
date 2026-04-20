from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.user import UserCreate, UserResponse, UserUpdate
from services import user as user_service

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("", response_model=List[UserResponse], summary="Obtener todos los usuarios", description="Retorna una lista de todos los usuarios registrados.")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users

@router.post("", response_model=UserResponse, summary="Crear un usuario", description="Registra un nuevo usuario en la base de datos.")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=UserResponse, summary="Obtener usuario por ID", description="Retorna los detalles de un usuario específico basado en su ID.")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserResponse, summary="Actualizar un usuario", description="Actualiza total o parcialmente los datos de un usuario por su ID.")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = user_service.update_user(db, user_id=user_id, user_data=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", summary="Eliminar un usuario", description="Elimina permanentemente un usuario de la base de datos.")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = user_service.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
