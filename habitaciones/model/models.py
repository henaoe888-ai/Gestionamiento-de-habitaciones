from sqlalchemy import Column, Integer, String  #Sacamos algunos elementos que incluye sqlalchemy y importamos 

from database import Base #Traemos de el archivo "database" a la clase Base

class Habitacion(Base): #Creacion de la clase Habitacion

    __tablename__ = "Habitaciones" #Nombramos a la tabla "Habitaciones"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, nullable=False)
    piso = Column(Integer, nullable=False)
    capacidad = Column(Integer , nullable=False)
    tipo = Column(String(50), nullable=False)
    precio = Column(Integer, nullable=False)

#Creamos los datos que requiera nuestra tabla o que iran en ella y adicional indicamos que son column con Column,
#Integer para numeros y String para texto esto con un cierto límite.

#primary_key=True, si es una clave primaria
#unique puede ser un dato con un unico numero o palabra
#nullable para indicar que el campo no puede ser nulo osea vacío