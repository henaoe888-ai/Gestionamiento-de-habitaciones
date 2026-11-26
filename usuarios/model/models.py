from sqlalchemy import Column, Integer, String  

from database import Base 

class Usuario(Base): 

    __tablename__ = "Usuarios" 

    id = Column(Integer, primary_key=True, index=True)
    nombre_completo = Column(String(40), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String (255),nullable=False)
