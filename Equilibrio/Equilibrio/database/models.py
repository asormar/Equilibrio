import reflex as rx
from sqlmodel import Field
from datetime import datetime


class ClientEntryModel(rx.Model, table=True):
    """Model for client entries."""
    
    name: str
    gender: str
    birth_date: str
    job: str
    email: str
    phone: str

class SecondaryDataModel(rx.Model, table=True):
    """Model for secondary data of clients."""
    
    direction: str
    country: str

class MeasurementModel(rx.Model, table=True):
    """Modelo para las mediciones de los clientes."""
    client_id: int = Field(foreign_key="cliententrymodel.id")
    date: str = Field(default_factory=lambda: datetime.utcnow().strftime("%d/%m/%Y"))
    weight: float
    height: float
    hip: float
    waist: float
