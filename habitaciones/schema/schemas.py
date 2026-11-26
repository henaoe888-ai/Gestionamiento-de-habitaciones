from pydantic import BaseModel, ConfigDict, Field  #de la herramienta pydantic importaremos algunos elementos como son el BaseModel,ConfigDict,Field

class HabitacionCreate(BaseModel): #definimos los atributos que queremos que en esten al momento de obtener, poner o actualizar los datos de el registro

    numero: int = Field(gt=0) #definimos tipo y ademas le decimos que sea mayor a 0
    piso: int = Field(gt=0) #definimos tipo y ademas le decimos que sea mayor a 0
    capacidad: int = Field(gt=0) #definimos tipo y ademas le decimos que sea mayor a 0
    tipo: str = Field(min_length=2, max_length=50) #definimos y le indicamos que como minimo tenga 2 y que como maximo 50 letras
    precio: int = Field(gt=0) #definimos tipo y ademas le decimos que sea mayor a 0

class HabitacionResponse(BaseModel): #aqui es donde pydantic nos ayuda a validar, que en la respuesta de cada metodo la devuelva de el tipo de dato definido

    id: int
    numero: int
    piso: int
    capacidad: int
    tipo: str
    precio: int

    model_config = ConfigDict(from_attributes=True)