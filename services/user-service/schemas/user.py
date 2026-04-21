from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from schemas.address import AddressResponse

class UserBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    activo: bool = True
    role: str = "user"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    addresses: List[AddressResponse] = []

    class Config:
        from_attributes = True

