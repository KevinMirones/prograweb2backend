from typing import Dict
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlmodel import Session
from app.core.database import CurrentContext
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteRead
from app.services.cliente_services import (
    create_new_cliente,
    get_active_cliente_by_id,
    get_all_active_clientes,
    update_existing_cliente,
    save_cliente_changes,
)


def handle_create_cliente(
    context: CurrentContext, data: ClienteCreate
) -> Dict[str, object]:
    session = context.current_session
    cliente = create_new_cliente(session, data)
    save_cliente_changes(session, cliente)

    return {
        "data": ClienteRead.model_validate(cliente),
        "msg": "Cliente creado exitosamente.",
    }


def handle_get_cliente(session: Session, cliente_id: int) -> Dict[str, object]:
    cliente = get_active_cliente_by_id(session, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    return {
        "data": ClienteRead.model_validate(cliente),
        "msg": "Cliente obtenido exitosamente.",
    }


def handle_list_clientes(session: Session) -> Dict[str, object]:
    clientes = get_all_active_clientes(session)
    return {"data": clientes, "msg": "Clientes obtenidos exitosamente."}


def handle_update_cliente(
    context: CurrentContext, cliente_id: int, data: ClienteUpdate
) -> Dict[str, object]:
    session = context.current_session

    cliente = get_active_cliente_by_id(session, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="cliente no encontrado.")
    updated_cliente = update_existing_cliente(session, cliente, data)
    save_cliente_changes(session, cliente)
    
    return {
        "data": ClienteRead.model_validate(updated_cliente),
        "msg": "Cliente actualizado exitosamente",
    }


def handle_delete_cliente(context: CurrentContext, cliente_id: int) -> Dict[str, object]:
    session = context.current_session
    cliente = get_active_cliente_by_id(session, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado.")
    cliente.is_deleted = True
    cliente.deleted_at = datetime.now(timezone.utc)
    save_cliente_changes(session, cliente)
    return {"msg": "Cliente eliminado exitosamente."}