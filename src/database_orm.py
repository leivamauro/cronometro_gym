#python
from datetime import datetime, timedelta
#terceros
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker,
)
from sqlalchemy import (
    String,
    Integer,
    ForeignKey,
    DateTime,
    Column,
    Boolean,
    create_engine,

)
#locales

#conxion a la base de datos
engine = create_engine("sqlite:///storage/data/gestion_pagos.db", echo=True)

class Base(DeclarativeBase):
    pass

class Miembro(Base):
    __tablename__ = "miembros"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    fecha_registro = Column(DateTime(), nullable=False, default=datetime.now())
    fecha_vencimiento = Column(DateTime())
    es_prueba = Column(Boolean(), default=True) # empieza como prueba por defecto

    def __str__(self):
        return self.nombre
    
    def _calcular_vencimiento(self, meses_abonados: int) -> datetime:
        # Definimos la fecha base de cálculo
        if self.fecha_vencimiento and self.fecha_vencimiento > datetime.now():
            fecha_base = self.fecha_vencimiento
        else:
            fecha_base = datetime.now()
            
        # relativedelta suma meses reales inteligentemente
        return fecha_base + relativedelta(months=meses_abonados)

class Configuracion(Base):
    __tablename__ = "configuraciones"

    clave = Column(String(255), primary_key=True)
    valor = Column(String(255), nullable=False)

    def __str__(self):
        return f"{self.clave}: {self.valor}"


class HistorialPago(Base):
    __tablename__ = "historial_pagos"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    miembro_id = Column(Integer(), ForeignKey("miembros.id"))
    fecha_pago = Column(DateTime(), nullable=False)
    monto = Column(Integer(),nullable=False)
    meses_abonados = Column(Integer(), default=1)

    def __str__(self):
        return f"Pago de {self.monto} el {self.fecha_pago} por {self.meses_abonados} meses"


# relacion entre la conexion y los modelos

Session = sessionmaker(engine)
session = Session()

if __name__ == "__main__":
    Base.metadata.create_all(engine) # crea todas las tablas de la base de datos
    # Base.metadata.drop_all(engine) # elmina toda la base de datos