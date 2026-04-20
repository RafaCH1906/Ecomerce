from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.address import AddressCreate, AddressResponse, AddressUpdate
from services import address as address_service
from services import user as user_service

router = APIRouter(tags=["Addresses"])

@router.get("/api/users/{user_id}/addresses", response_model=List[AddressResponse], summary="Obtener direcciones de un usuario", description="Retorna todas las direcciones asociadas a un usuario específico.")
def read_user_addresses(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return address_service.get_addresses_by_user(db, user_id=user_id)

@router.post("/api/users/{user_id}/addresses", response_model=AddressResponse, summary="Crear dirección para usuario", description="Añade una nueva dirección a la lista de direcciones de un usuario.")
def create_address_for_user(user_id: int, address: AddressCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return address_service.create_address(db=db, address=address, user_id=user_id)

@router.put("/api/addresses/{address_id}", response_model=AddressResponse, summary="Actualizar una dirección", description="Modifica los datos de una dirección existente por su ID.")
def update_address(address_id: int, address: AddressUpdate, db: Session = Depends(get_db)):
    db_address = address_service.update_address(db, address_id=address_id, address_data=address)
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@router.delete("/api/addresses/{address_id}", summary="Eliminar una dirección", description="Elimina una dirección del sistema.")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    success = address_service.delete_address(db, address_id=address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"detail": "Address deleted"}
