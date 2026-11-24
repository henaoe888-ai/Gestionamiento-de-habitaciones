from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Habitacion
from schemas import HabitacionCreate, HabitacionResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestion de habitaciones")

@app.get("/habitaciones", response_model=list[HabitacionResponse])
def get_habitaciones(
    tipo: str = None,
    db: Session = Depends(get_db)
):
    consulta = db.query(Habitacion)

    if tipo:
        consulta = consulta.filter(
            Habitacion.tipo.ilike(tipo.strip())
        )

    habitaciones = consulta.all()

    return habitaciones

@app.get("/habitaciones/{habitacion_id}", response_model=HabitacionResponse)
def get_person(
    habitacion_id: int,
    db: Session = Depends(get_db)
):
    habitacion = db.query(Habitacion).filter(
        Habitacion.id == habitacion_id
    ).first()

    if habitacion is None:
        raise HTTPException(
            status_code=404,
            detail="Habitación no encontrada"
        )
    
    return habitacion

@app.post("/habitaciones", response_model=HabitacionResponse, status_code=201)
def crear_habitacion(
    data: HabitacionCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Habitacion).filter(
        Habitacion.numero == data.numero
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Número de habitación ya registrado"
        )

    habitacion = Habitacion(
        numero=data.numero,
        piso=data.piso,
        capacidad=data.capacidad,
        tipo=data.tipo,
        precio=data.precio
    )

    db.add(habitacion)
    db.commit()
    db.refresh(habitacion)

    return habitacion

@app.put("/habitaciones/{habitacion_id}", response_model=HabitacionResponse)
def actualizar_habitacion(
    habitacion_id: int,
    data: HabitacionCreate,
    db: Session = Depends(get_db)
):
    habitacion = db.query(Habitacion).filter(
        Habitacion.id == habitacion_id
    ).first()

    if habitacion is None:
        raise HTTPException(
            status_code=404,
            detail="Habitacion no encontrada"
        )

    duplicated = db.query(Habitacion).filter(
        Habitacion.numero == data.numero,
        Habitacion.id != habitacion_id
    ).first()

    if duplicated:
        raise HTTPException(
            status_code=400,
            detail="Numero de habitacion, ya registyrado"
        )

    habitacion.numero = data.numero
    habitacion.piso = data.piso
    habitacion.capacidad = data.capacidad
    habitacion.tipo = data.tipo
    habitacion.precio = data.precio

    db.commit()
    db.refresh(habitacion)

    return habitacion

@app.delete("/habitaciones/{habitacion_id}")
def borrar_habitacion(
    habitacion_id: int,
    db: Session = Depends(get_db)
):
    habitacion = db.query(Habitacion).filter(
        Habitacion.id == habitacion_id
    ).first()

    if habitacion is None:
        raise HTTPException(
            status_code=404,
            detail="Habitacion no encontrada"
        )

    db.delete(habitacion)
    db.commit()

    return {
        "message": "Habitacion borrada exitosamente"
    }

