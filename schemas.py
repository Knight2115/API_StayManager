from pydantic import BaseModel
from decimal import Decimal
from datetime import date

class LoginRequest(BaseModel):
    usuario: str
    contraseña: str
    
class LoginResponse(BaseModel):
    mensaje: str
    rol: str | None = None
    EmpKey: int
    
class HotelIn(BaseModel):
    HotelID: int
    Nombre: str
    Cadena: str
    Ciudad: str
    Pais: str
    Estrellas: int
    Direccion: str

class HotelOut(BaseModel):
    HotelKey: int
    Nombre: str

    class Config:
        orm_mode = True
        
class ClienteIn(BaseModel):
    Nombre: str
    Apellido: str
    Genero: str
    Nacionalidad: str
    TipoCliente: str
        
class ClienteOut(BaseModel):
    ClienteKey: int
    Nombre: str
    Apellido: str
    Genero: str
    Nacionalidad: str
    TipoCliente: str

    class Config:
        orm_mode = True
        
class TipoHabOut(BaseModel):
    TipoHabKey: int
    Categoria: str
    TarifaEstandar: Decimal

    class Config:
        orm_mode = True

class HabitacionIn(BaseModel):
    HabitacionID: int
    HotelKey: int
    TipoHabKey: int
    NumeroHab: int
    Piso: int
    Capacidad: int
    Vista: bool

class HabitacionOut(BaseModel):
    HabitacionKey: int
    NumeroHab: int
    Capacidad: int
    TipoHab: TipoHabOut

    class Config:
        orm_mode = True
        
class FechaIn(BaseModel):
    Fecha: date
    Año: int
    Trimestre: int
    Mes: int
    Dia: int
    DiaSemana: str
    EsFinDeSemana: bool

class FechaOut(BaseModel):
    FechaKey: int
    Fecha: date
    Año: int
    Trimestre: int
    Mes: int
    Dia: int
    DiaSemana: str
    EsFinDeSemana: bool

    class Config:
        orm_mode = True
        
class CanalReservaOut(BaseModel):
    CanalKey: int
    NombreCanal: str

    class Config:
        orm_mode = True

class PagoOut(BaseModel):
    PagoKey: int
    Metodo: str

    class Config:
        orm_mode = True
        
class ReservaIn(BaseModel):
    HotelKey: int
    ClienteKey: int
    HabKey: int
    FechaKey: int
    EmpKey: int
    CanalKey: int
    PagoKey: int
    NochesReservadas: int
    CantidadHuespedes: int
    IngresoHabitacion: Decimal
    IngresoServicios: Decimal
    DescuentoTotal: Decimal
    ImpuestoTotal: Decimal
    LeadTimeReserva: int
    IngresoTotal: Decimal

    class Config:
        orm_mode = True

class ReservaOut(BaseModel):
    ReservaKey: int
    Hotel: HotelOut
    Cliente: ClienteOut
    Habitacion: HabitacionOut
    Fecha: FechaOut
    EmpKey: int
    CanalKey: int
    PagoKey: int
    NochesReservadas: int
    CantidadHuespedes: int
    IngresoHabitacion: Decimal
    IngresoServicios: Decimal
    DescuentoTotal: Decimal
    ImpuestoTotal: Decimal
    LeadTimeReserva: int
    IngresoTotal: Decimal

    class Config:
        orm_mode = True
