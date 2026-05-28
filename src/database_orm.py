#python
from datetime import datetime, timedelta
#terceros
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    sessionmaker,
)
from sqlalchemy import (
    String,
    Integer,
    Float,
    Numeric,
    ForeignKey,
    DateTime,
    Column,
    Boolean,
    create_engine,

)
#locales

#conxion a la base de datos
engine = create_engine("sqlite:///storage/data/gestion_pagos.db", echo=True)

# relacion entre la conexion y los modelos
SessionLocal = sessionmaker(engine)
session = SessionLocal()

class Base(DeclarativeBase):
    pass

class Miembro(Base):
    __tablename__ = "miembros"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    fecha_registro = Column(DateTime(), nullable=False, default=datetime.now())
    fecha_vencimiento = Column(DateTime())
    es_prueba = Column(Boolean(), default=True) # empieza como prueba por defecto
    tiempo_prueba_dias = Column(Integer(), default=0) # duracion de la prueba en dias, por defecto 1 dia

    def __str__(self):
        return self.nombre
    
class Configuracion(Base):
    __tablename__ = "configuraciones"

    clave = Column(String(55), primary_key=True)
    valor = Column(String(55), nullable=False)

    def __str__(self):
        return f"{self.clave}: {self.valor}"


class HistorialPago(Base):
    __tablename__ = "historial_pagos"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    miembro_id = Column(Integer(), ForeignKey("miembros.id"))
    fecha_pago = Column(DateTime(), nullable=False)
    monto = Column(Numeric(precision=10, scale=2), nullable=False)
    meses_abonados = Column(Integer(), default=1)

    def __str__(self):
        return f"Pago de {self.monto} el {self.fecha_pago} por {self.meses_abonados} meses"


# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def _ultimo_pago(miembro_id: int, session: Session) -> HistorialPago | None:
    """
    Retorna el último pago registrado para un miembro.
    ---
    Entrada:
        miembro_id (int): ID del miembro.
        session (Session): Sesión activa de SQLAlchemy.
    Salida:
        HistorialPago | None: Último pago o None si no hay registros.
    """
    return (
        session.query(HistorialPago)
        .filter_by(miembro_id=miembro_id)
        .order_by(HistorialPago.fecha_pago.desc())
        .first()
    )


def _inicio_ciclo_pago(miembro: Miembro) -> datetime:
    """
    Retorna la fecha en que empieza a contar el ciclo de pago.
    Si el miembro tiene días de prueba, se suma ese período a la fecha de registro.
    ---
    Entrada:
        miembro (Miembro): Instancia del miembro.
    Salida:
        datetime: Fecha de inicio del ciclo de pago.
    """
    if miembro.es_prueba and miembro.tiempo_prueba_dias > 0:
        return miembro.fecha_registro + timedelta(days=miembro.tiempo_prueba_dias)
    return miembro.fecha_registro


def _fecha_vencimiento(miembro: Miembro, session: Session) -> datetime:
    """
    Calcula la fecha de vencimiento acumulando todos los pagos del miembro.
    Cada pago extiende desde max(vencimiento_actual, fecha_pago) + meses_abonados.
    Si no hay pagos, toma la fecha de inicio del ciclo + 1 mes.
    ---
    Entrada:
        miembro (Miembro): Instancia del miembro.
        session (Session): Sesión activa de SQLAlchemy.
    Salida:
        datetime: Fecha de vencimiento calculada.
    """
    inicio = _inicio_ciclo_pago(miembro)
    ahora = datetime.now()

    # Si todavía está en período de prueba, la fecha de vencimiento es el futuro
    if miembro.es_prueba and miembro.tiempo_prueba_dias > 0 and ahora < inicio:
        return inicio + relativedelta(months=1)

    # Acumular todos los pagos ordenados cronológicamente
    pagos = (
        session.query(HistorialPago)
        .filter_by(miembro_id=miembro.id)
        .order_by(HistorialPago.fecha_pago.asc())
        .all()
    )

    if not pagos:
        # Sin pagos: vence 1 mes después del inicio
        return inicio + relativedelta(months=1)

    vencimiento = inicio
    for pago in pagos:
        base = max(vencimiento, pago.fecha_pago)
        vencimiento = base + relativedelta(months=pago.meses_abonados)

    return vencimiento


def _calcular_vencimiento(miembro: Miembro, session: Session) -> int:
    """
    Calcula cuántos meses completos está vencido el pago del miembro.
    0 significa que está al día.
    ---
    Entrada:
        miembro (Miembro): Instancia del miembro.
        session (Session): Sesión activa de SQLAlchemy.
    Salida:
        int: Cantidad de meses vencido (0 = al día).
    """
    ahora = datetime.now()

    # Si está en prueba, no está vencido
    inicio = _inicio_ciclo_pago(miembro)
    if miembro.es_prueba and miembro.tiempo_prueba_dias > 0 and ahora < inicio:
        return 0

    vencimiento = _fecha_vencimiento(miembro, session)

    if ahora <= vencimiento:
        return 0

    diff = relativedelta(ahora, vencimiento)
    return diff.months + (diff.years * 12)


def _esta_vencido(miembro: Miembro, session: Session) -> bool:
    """
    Verifica si el miembro tiene el pago vencido.
    ---
    Entrada:
        miembro (Miembro): Instancia del miembro.
        session (Session): Sesión activa de SQLAlchemy.
    Salida:
        bool: True si está vencido, False si está al día.
    """
    return _calcular_vencimiento(miembro, session) > 0


def _dias_restantes(miembro: Miembro, session: Session) -> int:
    """
    Retorna la cantidad de días que faltan para el vencimiento.
    Si ya está vencido, retorna 0.
    ---
    Entrada:
        miembro (Miembro): Instancia del miembro.
        session (Session): Sesión activa de SQLAlchemy.
    Salida:
        int: Días restantes (0 si ya venció).
    """
    if _esta_vencido(miembro, session):
        return 0

    vencimiento = _fecha_vencimiento(miembro, session)
    diff = vencimiento - datetime.now()
    return max(0, diff.days)


def _dias_pasados(miembro: Miembro, session: Session) -> int:
    """
    Retorna la cantidad de días que pasaron desde el vencimiento.
    Si no está vencido, retorna 0.
    ---
    Entrada:
        miembro (Miembro): Instancia del miembro.
        session (Session): Sesión activa de SQLAlchemy.
    Salida:
        int: Días transcurridos desde el vencimiento (0 si no venció).
    """
    if not _esta_vencido(miembro, session):
        return 0

    vencimiento = _fecha_vencimiento(miembro, session)
    diff = datetime.now() - vencimiento
    return max(0, diff.days)


if __name__ == "__main__":
    Base.metadata.create_all(engine) # crea todas las tablas de la base de datos
    # Base.metadata.drop_all(engine) # elmina toda la base de datos