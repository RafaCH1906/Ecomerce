from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.user import UserCreate, UserResponse, UserUpdate
from models.user import User
from services import user as user_service
from dependencies import get_current_user, get_current_admin_user

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("", response_model=List[UserResponse], summary="Obtener todos los usuarios", description="Retorna una lista de todos los usuarios registrados. Solo administradores.")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), admin_user: User = Depends(get_current_admin_user)):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users

@router.post("", response_model=UserResponse, summary="Crear un usuario", description="Registra un nuevo usuario en la base de datos. Público.")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return user_service.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=UserResponse, summary="Obtener usuario por ID", description="Retorna los detalles de un usuario específico. El usuario debe ser el propietario de la cuenta o un administrador.")
def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "superadmin"] and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para ver este perfil")
        
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@router.put("/{user_id}", response_model=UserResponse, summary="Actualizar un usuario", description="Actualiza datos de un usuario. El usuario debe ser el propietario o un administrador.")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "superadmin"]:
        if current_user.id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para editar este perfil")
        # Prevenir que un usuario normal se dé permisos de admin
        if user.role is not None and user.role != current_user.role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para cambiar tu propio rol")
            
    db_user = user_service.update_user(db, user_id=user_id, user_data=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@router.delete("/{user_id}", summary="Eliminar un usuario", description="Elimina permanentemente un usuario. Solo administradores.")
def delete_user(user_id: int, db: Session = Depends(get_db), admin_user: User = Depends(get_current_admin_user)):
    success = user_service.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"detail": "User deleted"}
