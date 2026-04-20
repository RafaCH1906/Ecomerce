from pydantic import BaseModel
from typing import Optional

class AddressBase(BaseModel):
    direccion: str
    ciudad: str
    pais: str
    codigo_postal: str
    principal: bool = False

class AddressCreate(AddressBase):
    pass

class AddressUpdate(BaseModel):
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    codigo_postal: Optional[str] = None
    principal: Optional[bool] = None

class AddressResponse(AddressBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

