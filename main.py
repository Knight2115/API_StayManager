from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import models
import schemas
import bcrypt

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

print("Rutas disponibles:")
from fastapi.routing import APIRoute
for route in app.routes:
    if isinstance(route, APIRoute):
        print(route.path)

# Dependencia para obtener sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# CORS: permitir acceso desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # O "*" para permitir todo durante desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login", response_model=schemas.LoginResponse)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.Credencial).filter(models.Credencial.Usuario == data.usuario).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    if not bcrypt.checkpw(data.contraseña.encode(), user.PasswordHash.encode()):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    if not user.Estado:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    return {
      "mensaje": "Inicio de sesión exitoso",
      "rol": user.Rol,
      "EmpKey": user.EmpKey
    }

@app.get("/reservas", response_model=List[schemas.ReservaOut])
def listar_reservas(db: Session = Depends(get_db)):
    try:
        reservas = db.query(models.Reservas)\
            .options(
                joinedload(models.Reservas.Hotel),
                joinedload(models.Reservas.Cliente),
                joinedload(models.Reservas.Habitacion),
                joinedload(models.Reservas.Fecha),
            ).limit(10).all()
        return reservas
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/hoteles", response_model=List[schemas.HotelOut])
def listar_hoteles(db: Session = Depends(get_db)):
    try:
        hoteles = db.query(models.Hotel).all()
        return hoteles
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/habitaciones/{hotel_id}", response_model=List[schemas.HabitacionOut])
def listar_habitaciones_por_hotel(hotel_id: int, db: Session = Depends(get_db)):
    try:
        habitaciones = db.query(models.Habitacion)\
            .options(joinedload(models.Habitacion.TipoHab))\
            .filter(models.Habitacion.HotelKey == hotel_id)\
            .all()
        return habitaciones
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()  
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/canal-reservas", response_model=List[schemas.CanalReservaOut])
def listar_canales_reserva(db: Session = Depends(get_db)):
    try:
        canales = db.query(models.CanalReserva).all()
        return canales
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/pagos", response_model=List[schemas.PagoOut])
def listar_pagos(db: Session = Depends(get_db)):
    try:
        pagos = db.query(models.Pago).all()
        return pagos
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/clientes", response_model=List[schemas.ClienteOut])
def listar_clientes(db: Session = Depends(get_db)):
    try:
        clientes = db.query(models.Cliente).limit(10).all()
        return clientes
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/nuevo-cliente", response_model=schemas.ClienteOut)
def crear_cliente(cliente: schemas.ClienteIn, db: Session = Depends(get_db)):
    try:
        nuevo_cliente = models.Cliente(
            Nombre=cliente.Nombre,
            Apellido=cliente.Apellido,
            Genero=cliente.Genero,
            Nacionalidad=cliente.Nacionalidad,
            TipoCliente=cliente.TipoCliente
        )
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)
        return nuevo_cliente

    except Exception as e:
        import traceback; traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/fechas", response_model=List[schemas.FechaOut])
def listar_fechas(db: Session = Depends(get_db)):
    try:
        fechas = db.query(models.Fecha).limit(10).all()
        return fechas
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/nueva-fecha", response_model=schemas.FechaOut)
def crear_fecha(fecha: schemas.FechaIn, db: Session = Depends(get_db)):
    try:
        existente = (
            db.query(models.Fecha)
              .filter(models.Fecha.Fecha == fecha.Fecha)
              .first()
        )
        if existente:
            return existente

        nueva_fecha = models.Fecha(
            Fecha=fecha.Fecha,
            Año=fecha.Año,
            Trimestre=fecha.Trimestre,
            Mes=fecha.Mes,
            Dia=fecha.Dia,
            DiaSemana=fecha.DiaSemana,
            EsFinDeSemana=fecha.EsFinDeSemana
        )
        db.add(nueva_fecha)
        db.commit()
        db.refresh(nueva_fecha)
        return nueva_fecha

    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No se pudo crear la fecha: {e}"
        )

@app.post("/nueva-reserva", response_model=schemas.ReservaOut, status_code=201)
def crear_reserva(reserva_in: schemas.ReservaIn, db: Session = Depends(get_db)):
    try:
        nueva = models.Reservas(
            HotelKey           = reserva_in.HotelKey,
            ClienteKey         = reserva_in.ClienteKey,
            HabKey             = reserva_in.HabKey,
            FechaKey           = reserva_in.FechaKey,
            EmpKey             = reserva_in.EmpKey,
            CanalKey           = reserva_in.CanalKey,
            PagoKey            = reserva_in.PagoKey,
            NochesReservadas   = reserva_in.NochesReservadas,
            CantidadHuespedes  = reserva_in.CantidadHuespedes,
            IngresoHabitacion  = reserva_in.IngresoHabitacion,
            IngresoServicios   = reserva_in.IngresoServicios,
            DescuentoTotal     = reserva_in.DescuentoTotal,
            ImpuestoTotal      = reserva_in.ImpuestoTotal,
            LeadTimeReserva    = reserva_in.LeadTimeReserva,
            IngresoTotal       = reserva_in.IngresoTotal
        )

        db.add(nueva)
        db.commit()
        db.refresh(nueva)

        return db.query(models.Reservas)\
                 .options(
                   joinedload(models.Reservas.Hotel),
                   joinedload(models.Reservas.Cliente),
                   joinedload(models.Reservas.Habitacion),
                   joinedload(models.Reservas.Fecha)
                 )\
                 .filter(models.Reservas.ReservaKey == nueva.ReservaKey)\
                 .first()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

from pydantic import BaseModel
from typing import Optional

class HotelIn(BaseModel):
    HotelID: Optional[int] = None
    Nombre: str
    Cadena: Optional[str] = None
    Ciudad: Optional[str] = None
    Pais: Optional[str] = None
    Estrellas: Optional[int] = None
    Direccion: Optional[str] = None

class HotelOut(HotelIn):
    HotelKey: int

    class Config:
        orm_mode = True

@app.post("/nuevo-hotel", response_model=schemas.HotelOut, status_code=201)
def crear_hotel(hotel_in: schemas.HotelIn, db: Session = Depends(get_db)):
    try:
        # Validar si ya existe un hotel con el mismo nombre
        existe = db.query(models.Hotel).filter(models.Hotel.Nombre == hotel_in.Nombre).first()
        if existe:
            raise HTTPException(status_code=400, detail="Ya existe un hotel con ese nombre")

        nuevo_hotel = models.Hotel(
            HotelID=hotel_in.HotelID,
            Nombre=hotel_in.Nombre,
            Cadena=hotel_in.Cadena,
            Ciudad=hotel_in.Ciudad,
            Pais=hotel_in.Pais,
            Estrellas=hotel_in.Estrellas,
            Direccion=hotel_in.Direccion
        )
        db.add(nuevo_hotel)
        db.commit()
        db.refresh(nuevo_hotel)
        return nuevo_hotel

    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/nueva-habitacion", response_model=schemas.HabitacionOut, status_code=201)
def crear_habitacion(habitacion_in: schemas.HabitacionIn, db: Session = Depends(get_db)):
    try:
        # Verificar si el hotel existe
        hotel = db.query(models.Hotel).filter(models.Hotel.HotelKey == habitacion_in.HotelKey).first()
        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel no encontrado")

        # Crear la nueva habitación
        nueva_habitacion = models.Habitacion(
            HabitacionID=habitacion_in.HabitacionID,
            HotelKey=habitacion_in.HotelKey,
            TipoHabKey=habitacion_in.TipoHabKey,
            NumeroHab=habitacion_in.NumeroHab,
            Piso=habitacion_in.Piso,
            Capacidad=habitacion_in.Capacidad,
            Vista=habitacion_in.Vista
        )

        db.add(nueva_habitacion)
        db.commit()
        db.refresh(nueva_habitacion)

        return nueva_habitacion
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la habitación: {str(e)}")
    
@app.get("/tipoHab", response_model=List[schemas.TipoHabOut])
def litas_tipoHab(db: Session = Depends(get_db)):
    try:
        tipoHab = db.query(models.TipoHab).limit(10).all()
        return tipoHab
    except Exception as e:
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))