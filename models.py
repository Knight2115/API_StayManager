from sqlalchemy import Column, Integer, String, Boolean, Numeric, Date, ForeignKey, text
from database import Base
from sqlalchemy.orm import relationship

class Credencial(Base):
    __tablename__ = 'credencial'
    CredencialKey = Column(Integer, primary_key=True, index=True)
    EmpKey = Column(Integer, ForeignKey('empleado.EmpleadoKey'))
    Usuario = Column(String, unique=True, index=True)
    PasswordHash = Column(String)
    Rol = Column(String, default='empleado')
    Estado = Column(Boolean, default=True)
    
class Hotel(Base):
    __tablename__ = 'hotel'
    HotelKey = Column(Integer, primary_key=True, index=True)
    HotelID = Column(Integer)
    Nombre = Column(String, unique=True, index=True)
    Cadena = Column(String)
    Ciudad = Column(String)
    Pais = Column(String)
    Estrellas = Column(Integer)
    Direccion = Column(String)
    
class Cliente(Base):
    __tablename__ = 'cliente'
    ClienteKey = Column(Integer, primary_key=True, index=True)
    ClienteID = Column(Integer, server_default=text("nextval('cliente_id_seq')"), nullable=False)
    Nombre = Column(String)
    Apellido = Column(String)
    Genero = Column(String)
    Nacionalidad = Column(String)
    TipoCliente = Column(String)
    
class TipoHab(Base):
    __tablename__ = 'tipoHab'
    TipoHabKey = Column(Integer, primary_key=True, index=True)
    TipoHabID = Column(Integer)
    Descripcion = Column(String)
    Categoria = Column(String)
    CapacidadMax = Column(Integer)
    TarifaEstandar = Column(Numeric(10, 2))

class Habitacion(Base):
    __tablename__ = 'habitacion'
    HabitacionKey = Column(Integer, primary_key=True, index=True)
    HabitacionID = Column(Integer)
    HotelKey = Column(Integer, ForeignKey('hotel.HotelKey'))
    TipoHabKey = Column(Integer, ForeignKey('tipoHab.TipoHabKey'))
    NumeroHab = Column(Integer)
    Piso = Column(Integer)
    Capacidad = Column(Integer)
    Vista = Column(Boolean)
    
    TipoHab = relationship("TipoHab")
    
class Fecha(Base):
    __tablename__ = 'fecha'
    FechaKey = Column(Integer, primary_key=True, index=True)
    Fecha = Column(Date)
    Año = Column(Integer)
    Trimestre = Column(Integer)
    Mes = Column(Integer)
    Dia = Column(Integer)
    DiaSemana = Column(String)
    EsFinDeSemana = Column(Boolean)
    
class CanalReserva(Base):
    __tablename__ = 'canalReserva'
    CanalKey = Column(Integer, primary_key=True, index=True)
    CanalID = Column(Integer)
    NombreCanal = Column(String)
    Descripcion = Column(String)
    
class Pago(Base):
    __tablename__ = 'pago'
    PagoKey = Column(Integer, primary_key=True, index=True)
    PagoID = Column(Integer)
    Metodo = Column(String)
    Moneda = Column(String)
    
class Empleado(Base):
    __tablename__ = 'empleado'
    EmpleadoKey = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String)
    Apellido = Column(String)
    Puesto = Column(String)
    Departamento = Column(String)
    FechaContratacion = Column(Date)
    HotelKey = Column(Integer, ForeignKey('hotel.HotelKey'))

class Reservas(Base):
    __tablename__ = 'reservas'
    ReservaKey = Column(Integer, primary_key=True, index=True)
    HotelKey = Column(Integer, ForeignKey('hotel.HotelKey'))
    ClienteKey = Column(Integer, ForeignKey('cliente.ClienteKey'))
    HabKey = Column(Integer, ForeignKey('habitacion.HabitacionKey'))
    FechaKey = Column(Integer, ForeignKey('fecha.FechaKey'))
    EmpKey = Column(Integer, ForeignKey('empleado.EmpleadoKey'))
    CanalKey = Column(Integer, ForeignKey('canalReserva.CanalKey'))
    PagoKey = Column(Integer, ForeignKey('pago.PagoKey'))
    NochesReservadas = Column(Integer)
    CantidadHuespedes = Column(Integer)
    IngresoHabitacion = Column(Numeric(10, 2))
    IngresoServicios = Column(Numeric(10, 2))
    DescuentoTotal = Column(Numeric(10, 2))
    ImpuestoTotal = Column(Numeric(10, 2))
    LeadTimeReserva = Column(Integer)
    IngresoTotal = Column(Numeric(10, 2))
    
    Hotel = relationship("Hotel")
    Cliente = relationship("Cliente")
    Habitacion = relationship("Habitacion")
    Fecha = relationship("Fecha")
    Empleado = relationship("Empleado")
    CanalReserva = relationship("CanalReserva")
    Pago = relationship("Pago")
