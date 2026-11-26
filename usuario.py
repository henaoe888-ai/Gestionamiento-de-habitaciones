from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from usuarios.model.models import Usuario
from usuarios.schema.schemas import UsuarioCreate, UsuarioResponse
from usuarios.security import crear_hash

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestionamiento de Usuarios")

@app.get("/usuarios", response_model=list[UsuarioResponse])
def ver_personas(db: Session = Depends(get_db)):
    usuario = db.query(Usuario).all()
    return usuario


# ====================================
# GET: Consultar una persona
# ====================================
@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def ver_persona(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrada"
        )

    return usuario


# ====================================
# POST: Registrar una persona
# ====================================
@app.post("/usuarios", response_model=UsuarioResponse, status_code=201)
def crear_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db)
):
    # Validar que el correo no esté registrado
    existing = db.query(Usuario).filter(
        Usuario.correo == data.correo
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="correo ya registrado"
        )

    usuario = Usuario(
        nombre_completo=data.nombre_completo,
        correo=data.correo,
        contraseña=crear_hash(data.contraseña)
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


# ====================================
# PUT: Actualizar una persona
# ====================================
@app.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: int,
    data: UsuarioCreate,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    # Validar que el correo no pertenezca a otra persona
    duplicated = db.query(Usuario).filter(
        Usuario.correo == data.correo,
        Usuario.id != usuario_id
    ).first()

    if duplicated:
        raise HTTPException(
            status_code=400,
            detail="Correo ya registrado"
        )

    usuario.nombre_completo = data.nombre_completo
    usuario.correo = data.correo
    usuario.contraseña = data.contraseña

    db.commit()
    db.refresh(usuario)

    return usuario


# ====================================
# DELETE: Eliminar una persona
# ====================================
@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Persona no encontrado"
        )

    db.delete(usuario)
    db.commit()

    return {
        "message": "usuario eliminado exitosamente"
    }