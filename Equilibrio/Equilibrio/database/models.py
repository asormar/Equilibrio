import reflex as rx

class ClientEntryModel(rx.Model, table=True):
    """Model for client entries."""
    
    name: str
    gender: str
    birth_date: str
    job: str
    email: str
    phone: str