from typing import Dict
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlmodel import Session
from app.core.database import CurrentContext
from app.schemas.tipo_equipo import TipoEquipoCreate, TipoEquipoUpdate, TipoEquipoRead
from app.services.tipo_equipo_services import (
    create_new_tipo,
    get_active_tipo_by_id,
    get_all_active_tipos,
    update_existing_tipo,
    save_tipo_changes,
)


def handle_create_tipo(context: CurrentContext, data: TipoEquipoCreate) -> Dict[str, object]:
    session = context.current_session
    tipo = create_new_tipo(session, data)
    save_tipo_changes(session, tipo)

    return {"data": TipoEquipoRead.model_validate(tipo), "msg": "Tipo de equipo creado exitosamente."}


def handle_get_tipo(session: Session, tipo_id: int) -> Dict[str, object]:
    tipo = get_active_tipo_by_id(session, tipo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de equipo no encontrado.")
    return {"data": TipoEquipoRead.model_validate(tipo), "msg": "Tipo obtenido exitosamente."}


def handle_list_tipos(session: Session) -> Dict[str, object]:
    tipos = get_all_active_tipos(session)
    return {"data": tipos, "msg": "Tipos obtenidos exitosamente."}


def handle_update_tipo(context: CurrentContext, tipo_id: int, data: TipoEquipoUpdate) -> Dict[str, object]:
    session = context.current_session

    tipo = get_active_tipo_by_id(session, tipo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de equipo no encontrado.")
    updated_tipo = update_existing_tipo(session, tipo, data)
    save_tipo_changes(session, tipo)

    return {"data": TipoEquipoRead.model_validate(updated_tipo), "msg": "Tipo actualizado exitosamente"}


def handle_delete_tipo(context: CurrentContext, tipo_id: int) -> Dict[str, object]:
    session = context.current_session
    tipo = get_active_tipo_by_id(session, tipo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de equipo no encontrado.")
    tipo.is_deleted = True
    tipo.deleted_at = datetime.now(timezone.utc)
    save_tipo_changes(session, tipo)
    return {"msg": "Tipo eliminado exitosamente."}
