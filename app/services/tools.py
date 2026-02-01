from sqlmodel import Session
from app.schemas.cliente import Cliente
from app.schemas.servicio import Servicio

def create_client_tool(db: Session, nombre: str, apellido_paterno: str, apellido_materno: str, telefono: str = None) -> str:
    """
    Creates a new client in the database.
    """
    try:
        new_client = Cliente(
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            telefono=telefono
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return f"Client created successfully with ID: {new_client.id}"
    except Exception as e:
        return f"Error creating client: {str(e)}"

def create_service_tool(db: Session, nombre: str, descripcion: str, precio: float) -> str:
    """
    Creates a new service in the database.
    """
    try:
        new_service = Servicio(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio
        )
        db.add(new_service)
        db.commit()
        db.refresh(new_service)
        return f"Service created successfully with ID: {new_service.id}"
    except Exception as e:
        return f"Error creating service: {str(e)}"

from app.schemas.equipo import Equipo
from app.schemas.tecnico import Tecnico
from app.schemas.tipo_equipo import TipoEquipo
from app.schemas.cotizacion import Cotizacion
from datetime import datetime

def create_tipo_equipo_tool(db: Session, nombre: str, descripcion: str) -> str:
    """Creates a new equipment type (e.g., Laptop, Printer)."""
    try:
        new_type = TipoEquipo(nombre=nombre, descripcion=descripcion)
        db.add(new_type)
        db.commit()
        db.refresh(new_type)
        return f"Equipment Type created with ID: {new_type.id}"
    except Exception as e:
        return f"Error creating equipment type: {str(e)}"

def create_tecnico_tool(db: Session, nombre: str, apellido_paterno: str, apellido_materno: str, telefono: str = None) -> str:
    """Registers a new technician."""
    try:
        new_tech = Tecnico(
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            telefono=telefono,
            fecha_ingreso=datetime.now()
        )
        db.add(new_tech)
        db.commit()
        db.refresh(new_tech)
        return f"Technician registered with ID: {new_tech.id}"
    except Exception as e:
        return f"Error registering technician: {str(e)}"

def create_equipo_tool(db: Session, marca: str, modelo: str, id_tipo_equipo: int, id_dueno: int) -> str:
    """Registers a new piece of equipment for a client."""
    try:
        # Validate existence of relationships could be added here, but DB will throw FK error usually
        new_device = Equipo(
            marca=marca,
            modelo=modelo,
            id_tipo_equipo=id_tipo_equipo,
            id_dueno=id_dueno
        )
        db.add(new_device)
        db.commit()
        db.refresh(new_device)
        return f"Equipment registered with ID: {new_device.id}"
    except Exception as e:
        return f"Error registering equipment: {str(e)}"

def create_cotizacion_tool(db: Session, id_cliente: int, id_equipo: int, descripcion_falla: str) -> str:
    """Creates a new quote request for a service."""
    try:
        new_quote = Cotizacion(
            id_cliente=id_cliente,
            id_equipo=id_equipo,
            descripcion_falla=descripcion_falla,
            estado="PENDIENTE" # Default state? Assuming string based on schema inspection
        )
        db.add(new_quote)
        db.commit()
        db.refresh(new_quote)
        return f"Quote created successfully with ID: {new_quote.id}"
    except Exception as e:
        return f"Error creating quote: {str(e)}"
