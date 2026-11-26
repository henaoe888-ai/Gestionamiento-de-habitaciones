from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from habitaciones.model.models import Habitacion
from habitaciones.schema.schemas import HabitacionCreate, HabitacionResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestion de habitaciones")

#--------- VER HABITACIONES Y BUSCA HABITACIONES CON UN CIERTO FILTRO ------------------
@app.get("/habitaciones", response_model=list[HabitacionResponse])
def ver_habitaciones(
    tipo: str = None, #indica que se puede ingresar un tipo de habitacion desde la url, pero si no se manda esta va a quedar vacia y no se buscara nada
    db: Session = Depends(get_db)
):
    consulta = db.query(Habitacion) #consulta todas los registros en este caso las habitaciones

    if tipo: #indica si se ingreso un tipo de habitacion
        consulta = consulta.filter( #filtra los datos segun la condicion que se implemente ("buscar por ejemplo con la palabra: matrimonial")
            Habitacion.tipo.ilike(tipo.strip()) #realiza la consulta y con ilike lo que hace esque busca matrimonial sin importar la que hallan may y min mezcladas
        )

    habitaciones = consulta.all() #consulta todas las habitaciones con la palabra por ejemplo "matrimonial"

    return habitaciones #devuelve el registro que ha sido consultado


#------------- BUSCA UNA HABITACION EN ESPECIFICO A TRÁVES DE EL ID --------------------
@app.get("/habitaciones/{habitacion_id}", response_model=HabitacionResponse)
def ver_habitacion(
    habitacion_id: int,
    db: Session = Depends(get_db)
):
    habitacion = db.query(Habitacion).filter( # realizamos una consulta de todo y a traves del filtro ponemos la condicion
        Habitacion.id == habitacion_id #indicamos que si el id que ingresamos, al momento de ver el registro el id debe coincidir con el id ingresado
    ).first() #lo encuentra

    if habitacion is None: 
        raise HTTPException(
            status_code=404,
            detail="Habitación no encontrada"  #si la habitacion esta vacia, generara ese mensaje con el numero de ese error
        )
    
    return habitacion #nos devuelve la vista de esa habitacion que queremos


#-----------CREAMOS UN REGISTRO DE UNA HABITACION ----------------------
@app.post("/habitaciones", response_model=HabitacionResponse, status_code=201)
def crear_habitacion(
    data: HabitacionCreate, #recibe los datos que se estan ingresando
    db: Session = Depends(get_db)
):
    existing = db.query(Habitacion).filter( #consulta la tabla habitaciones y pasa por filtra
        Habitacion.numero == data.numero #verifica si el numero de habitacion ya esta registrado
    ).first() #si no hay numeros repetidos, procede a crear el registro

    if existing: #comprueba si ya esta existente una habitacion con dicho numero
        raise HTTPException(
            status_code=400,
            detail="Número de habitación ya registrado"  #si ya el numero lo tienen, muestra mensaje de "ya registrado"
        )

    habitacion = Habitacion(  #a estos parametros, les estaremos poniendo datos
        numero=data.numero,
        piso=data.piso,
        capacidad=data.capacidad,
        tipo=data.tipo,
        precio=data.precio
    )

    db.add(habitacion) #agrega los datos ingresados y los prepara para enviar a una sesion de base de datos
    db.commit() #guarda los datos y los manda a la base de datos
    db.refresh(habitacion)  #actualiza el objeto Habitacion con la informacion ingresada, incluyendo el id

    return habitacion #nos devuelve el registro con sus respectivos datos y con su id asignado

#---------ACTUALIZAMOS UN REGISTRO DE UNA HABITACION -------------------
@app.put("/habitaciones/{habitacion_id}", response_model=HabitacionResponse)
def actualizar_habitacion(
    habitacion_id: int,
    data: HabitacionCreate,
    db: Session = Depends(get_db)
):
    habitacion = db.query(Habitacion).filter( #realiza una consulta de una habitacion con su id
        Habitacion.id == habitacion_id #el numero de id debe coincidir con el que pongamos en el que nosotros estemos ingresando
    ).first() #encuentra el id

    if habitacion is None: 
        raise HTTPException(
            status_code=404,  
            detail="Habitacion no encontrada"   #si la habitacion esta vacia, aparecera el mensaje de "no encontrada"
        )

    duplicated = db.query(Habitacion).filter( #consulta en la habitacion que no este usando un mismo numero de habitacion
        Habitacion.numero == data.numero, #reemplaza el numero anterior por el nuevo que se esta ingresando
        Habitacion.id != habitacion_id
    ).first()

    if duplicated:
        raise HTTPException(
            status_code=400,
            detail="Numero de habitacion, ya registrado"
        )

    habitacion.numero = data.numero       #lo mismo estaria pasando con estos parametros, se esta reeemplazando el dato viejo por el nuevo que se ingresa
    habitacion.piso = data.piso
    habitacion.capacidad = data.capacidad
    habitacion.tipo = data.tipo
    habitacion.precio = data.precio

    db.commit() #se guarda los cambios que se hicieron
    db.refresh(habitacion) #actualiza la informacion, y aparece la informacion nueva

    return habitacion #nos devuelve el registro con los datos ya cambiados

#--------ELIMINAR ALGUNOS REGISTROS --------------------
@app.delete("/habitaciones/{habitacion_id}")
def borrar_habitacion(
    habitacion_id: int,
    db: Session = Depends(get_db)
):
    habitacion = db.query(Habitacion).filter( #realizamos una consulta con su filtro en donde:
        Habitacion.id == habitacion_id   #se indique que registro queremos eliminar poniendo el id
    ).first() #encontramos la consulta

    if habitacion is None:
        raise HTTPException(
            status_code=404,
            detail="Habitacion no encontrada"  #ahora si la habitacion no existe, logicamente no podemos eliminarla y nos aparecera este mensaje de error
        )

    db.delete(habitacion) #eliminamos el registro
    db.commit() #se guarda el cambio que hicimos de eliminar la habitacion

    return {
        "message": "Habitacion borrada exitosamente" #y aparece este mensaje indicandonos que se borro exitosamente
    }
