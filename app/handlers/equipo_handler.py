from typing import Dict
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlmodel import Session
from app.core.database import CurrentContext
from app.schemas.equipo import EquipoCreate, EquipoUpdate, EquipoRead
from app.services.equipo_services import (
    create_new_equipo,
    get_active_equipo_by_id,
    get_all_active_equipos,
    update_existing_equipo,
    save_equipo_changes,
)


def handle_create_equipo(context: CurrentContext, data: EquipoCreate) -> Dict[str, object]:
    session = context.current_session
    equipo = create_new_equipo(session, data)
    save_equipo_changes(session, equipo)

    return {"data": EquipoRead.model_validate(equipo), "msg": "Equipo creado exitosamente."}


def handle_get_equipo(session: Session, equipo_id: int) -> Dict[str, object]:
    equipo = get_active_equipo_by_id(session, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado.")
    return {"data": EquipoRead.model_validate(equipo), "msg": "Equipo obtenido exitosamente."}


def handle_list_equipos(session: Session) -> Dict[str, object]:
    equipos = get_all_active_equipos(session)
    return {"data": equipos, "msg": "Equipos obtenidos exitosamente."}


def handle_update_equipo(context: CurrentContext, equipo_id: int, data: EquipoUpdate) -> Dict[str, object]:
    session = context.current_session

    equipo = get_active_equipo_by_id(session, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado.")
    updated_equipo = update_existing_equipo(session, equipo, data)
    save_equipo_changes(session, equipo)

    return {"data": EquipoRead.model_validate(updated_equipo), "msg": "Equipo actualizado exitosamente"}


def handle_delete_equipo(context: CurrentContext, equipo_id: int) -> Dict[str, object]:
    session = context.current_session
    equipo = get_active_equipo_by_id(session, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado.")
    equipo.is_deleted = True
    equipo.deleted_at = datetime.now(timezone.utc)
    save_equipo_changes(session, equipo)
    return {"msg": "Equipo eliminado exitosamente."}
