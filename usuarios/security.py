from passlib.context import CryptContext

# Configuración del hash
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# Función para encriptar
def crear_hash(contraseña: str):
    return pwd_context.hash(contraseña)

# Función para verificar
def verificar_contraseña(contraseña: str, contraseña_hash: str):
    return pwd_context.verify(contraseña, contraseña_hash)

