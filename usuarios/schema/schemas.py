from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UsuarioCreate(BaseModel):
    nombre_completo: str = Field(min_length=10,max_length=40)
    correo: EmailStr
    contraseña: str = Field(min_length=10,max_length=45)

class UsuarioResponse(BaseModel):
    id: int
    nombre_completo: str
    correo: str
    contraseña: str

    model_config = ConfigDict(from_attributes=True)


