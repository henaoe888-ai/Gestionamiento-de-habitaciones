from pydantic import BaseModel, ConfigDict, Field

class HabitacionCreate(BaseModel):
    numero: int = Field(gt=0)
    piso: int = Field(gt=0)
    capacidad: int = Field(gt=0)
    tipo: str = Field(min_length=2, max_length=50)
    precio: int = Field(gt=0)

class HabitacionResponse(BaseModel):
    id: int
    numero: int
    piso: int
    capacidad: int
    tipo: str
    precio: int

    model_config = ConfigDict(from_attributes=True)