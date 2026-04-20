from sqlalchemy.orm import Session
from models import user as md_user
from schemas import user as sc_user

def get_user(db: Session, user_id: int):
    return db.query(md_user.User).filter(md_user.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(md_user.User).filter(md_user.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(md_user.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: sc_user.UserCreate):
    # En producción: hashear password!
    db_user = md_user.User(
        nombre=user.nombre,
        email=user.email,
        password=user.password, # hash needed
        telefono=user.telefono,
        activo=user.activo
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_data: sc_user.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

