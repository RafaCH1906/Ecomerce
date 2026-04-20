from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    direccion = Column(String)
    ciudad = Column(String)
    pais = Column(String)
    codigo_postal = Column(String)
    principal = Column(Boolean, default=False)

    owner = relationship("User", back_populates="addresses")

