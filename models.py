from sqlalchemy import Column, Integer, String

from database import Base

class Habitacion(Base):

    __tablename__ = "Habitaciones"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, nullable=False)
    piso = Column(Integer, nullable=False)
    capacidad = Column(Integer , nullable=False)
    tipo = Column(String(50), nullable=False)
    precio = Column(Integer, nullable=False)

    #ID, número de habitación, piso, capacidad, tipo de habitación y precio por noche.