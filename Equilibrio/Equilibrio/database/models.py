import reflex as rx
from sqlmodel import Field

class ClientEntryModel(rx.Model, table=True):
    """Model for client entries."""
    
    name: str
    gender: str
    birth_date: str
    job: str
    email: str
    phone: str

class MeasurementModel(rx.Model, table=True):
    """Modelo para las mediciones de los clientes."""
    client_id: int = Field(foreign_key="cliententrymodel.id")
    date: str  # o datetime.date si estás usando tipos nativos
    weight: float
    height: float
    hip: float
    waist: float
