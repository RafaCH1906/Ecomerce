from sqlalchemy.orm import Session
from models import address as md_address
from schemas import address as sc_address

def get_address(db: Session, address_id: int):
    return db.query(md_address.Address).filter(md_address.Address.id == address_id).first()

def get_addresses_by_user(db: Session, user_id: int):
    return db.query(md_address.Address).filter(md_address.Address.user_id == user_id).all()

def create_address(db: Session, address: sc_address.AddressCreate, user_id: int):
    db_address = md_address.Address(**address.model_dump(), user_id=user_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def update_address(db: Session, address_id: int, address_data: sc_address.AddressUpdate):
    db_address = get_address(db, address_id)
    if db_address:
        update_dict = address_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int):
    db_address = get_address(db, address_id)
    if db_address:
        db.delete(db_address)
        db.commit()
        return True
    return False

