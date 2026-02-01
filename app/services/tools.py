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
