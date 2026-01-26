from enum import Enum
from typing import Optional
from datetime import datetime, timezone
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, text

from app.enums.estado_equipo_enum import EstadoEquipoEnum
from app.schemas.cliente import ClienteRead
from app.schemas.tipo_equipo import TipoEquipoRead


class Equipo(SQLModel, table=True):
    __tablename__ = "equipos"
    id: Optional[int] = Field(
        default=None, sa_column=Column("id_equ", Integer, primary_key=True)
    )
    marca: str = Field(sa_column=Column("marca_equ", String(255), nullable=False))
    modelo: str = Field(sa_column=Column("modelo_equ", String(255), nullable=False))
    id_tipo_equipo: int = Field(
        sa_column=Column("id_tipo_equipo_equ", Integer, ForeignKey("tipos_equipo.id_teq"))
    )
    id_dueno: int = Field(
        sa_column=Column("id_dueno_equ", Integer, ForeignKey("clientes.id_cli"))
    )
    estado: Optional[EstadoEquipoEnum] = Field(
        default=None, sa_column=Column("estado_equ", String(255), nullable=True)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "created_at_equ",
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            "updated_at_equ",
            DateTime(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column("deleted_at_equ", DateTime(timezone=True), nullable=True),
    )
    is_deleted: bool = Field(
        default=False,
        sa_column=Column("is_deleted_equ", Boolean, nullable=False, server_default="0"),
    )
    tipo_equipo: Optional["TipoEquipo"] = Relationship(back_populates="equipos")
    dueno: Optional["Cliente"] = Relationship(back_populates="equipos")
    cotizaciones: Optional["Cotizacion"] = Relationship(back_populates="equipo")


class EquipoCreate(SQLModel):
    marca: str
    modelo: str
    id_tipo_equipo: int
    id_dueno: int
    
class EquipoUpdate(SQLModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    id_tipo_equipo: Optional[int] = None
    id_dueno: Optional[int] = None
    estado: Optional[EstadoEquipoEnum] = None
    
class EquipoRead(SQLModel):
    id: int
    marca: str
    modelo: str
    tipo_equipo: Optional[TipoEquipoRead] = None
    dueno: Optional[ClienteRead] = None
    estado: Optional[EstadoEquipoEnum] = None
    created_at: datetime
    

    