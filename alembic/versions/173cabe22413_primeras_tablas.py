"""primeras tablas

Revision ID: 173cabe22413
Revises:
Create Date: 2026-01-25 17:01:04.799130
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '173cabe22413'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ---------------- CLIENTES ----------------
    op.create_table(
        'clientes',
        sa.Column('id_cli', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nombre_cli', sa.String(255), nullable=False),
        sa.Column('apellido_paterno_cli', sa.String(255), nullable=False),
        sa.Column('apellido_materno_cli', sa.String(255), nullable=False),
        sa.Column('telefono_cli', sa.String(20)),
        sa.Column(
            'created_at_cli',
            sa.TIMESTAMP(),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False
        ),
        sa.Column(
            'updated_at_cli',
            sa.DateTime(),
            nullable=False
        ),
        sa.Column('deleted_at_cli', sa.DateTime(), nullable=True),
        sa.Column('is_deleted_cli', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    )

    # ---------------- SERVICIOS ----------------
    op.create_table(
        'servicios',
        sa.Column('id_ser', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nombre_ser', sa.String(255), nullable=False),
        sa.Column('descripcion_ser', sa.String(255), nullable=False),
        sa.Column('precio_ser', sa.String(255), nullable=False),
        sa.Column(
            'created_at_ser',
            sa.TIMESTAMP(),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False
        ),
        sa.Column(
            'updated_at_ser',
            sa.DateTime(),
            nullable=False
        ),
        sa.Column('deleted_at_ser', sa.DateTime(), nullable=True),
        sa.Column('is_deleted_ser', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    )

    # ---------------- TECNICOS ----------------
    op.create_table(
        'tecnicos',
        sa.Column('id_tec', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nombre_tec', sa.String(255), nullable=False),
        sa.Column('apellido_paterno_tec', sa.String(255), nullable=False),
        sa.Column('apellido_materno_tec', sa.String(255), nullable=False),
        sa.Column('telefono_tec', sa.String(20)),
        sa.Column('fecha_ingreso_tec', sa.DateTime(), nullable=True),
        sa.Column(
            'created_at_tec',
            sa.TIMESTAMP(),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False
        ),
        sa.Column(
            'updated_at_tec',
            sa.DateTime(),
            nullable=False
        ),
        sa.Column('deleted_at_tec', sa.DateTime(), nullable=True),
        sa.Column('is_deleted_tec', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    )

    # ---------------- TIPOS EQUIPO ----------------
    op.create_table(
        'tipos_equipo',
        sa.Column('id_teq', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nombre_teq', sa.String(255), nullable=False),
        sa.Column('descripcion_teq', sa.String(255), nullable=False),
        sa.Column(
            'created_at_teq',
            sa.TIMESTAMP(),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False
        ),
        sa.Column(
            'updated_at_teq',
            sa.DateTime(),
            nullable=False
        ),
        sa.Column('deleted_at_teq', sa.DateTime(), nullable=True),
        sa.Column('is_deleted_teq', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    )

    # ---------------- EQUIPOS ----------------
    op.create_table(
        'equipos',
        sa.Column('id_equ', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('marca_equ', sa.String(255), nullable=False),
        sa.Column('modelo_equ', sa.String(255), nullable=False),
        sa.Column('id_tipo_equipo_equ', sa.Integer(), sa.ForeignKey('tipos_equipo.id_teq')),
        sa.Column('id_dueno_equ', sa.Integer(), sa.ForeignKey('clientes.id_cli')),
        sa.Column('estado_equ', sa.String(255)),
        sa.Column(
            'created_at_equ',
            sa.TIMESTAMP(),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False
        ),
        sa.Column(
            'updated_at_equ',
            sa.DateTime(),
            nullable=False
        ),
        sa.Column('deleted_at_equ', sa.DateTime(), nullable=True),
        sa.Column('is_deleted_equ', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    )

    # ---------------- TRABAJOS ----------------
    op.create_table(
        'trabajos',
        sa.Column('id_tra', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('descripcion_tra', sa.String(255), nullable=False),
        sa.Column('estado_tra', sa.String(255)),
        sa.Column('fecha_inicio_tra', sa.DateTime(), nullable=False),
        sa.Column('fecha_fin_tra', sa.DateTime(), nullable=True),
        sa.Column('costo_tra', sa.String(255), nullable=False),
        sa.Column('id_tecnico_tra', sa.Integer(), sa.ForeignKey('tecnicos.id_tec'), nullable=False),
        sa.Column(
            'created_at_tra',
            sa.TIMESTAMP(),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False
        ),
        sa.Column(
            'updated_at_tra',
            sa.DateTime(),
            nullable=False
        ),
        sa.Column('deleted_at_tra', sa.DateTime(), nullable=True),
        sa.Column('is_deleted_tra', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    )

    # ---------------- COTIZACIONES ----------------
    op.create_table(
        'cotizaciones',
        sa.Column('id_cot', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('id_cliente_cot', sa.Integer(), sa.ForeignKey('clientes.id_cli')),
        sa.Column('descripcion_falla_cot', sa.String(255), nullable=False),
        sa.Column('diagnostico_cot', sa.String(255)),
        sa.Column('fecha_expiracion_cot', sa.DateTime()),
        sa.Column('id_tecnico_cot', sa.Integer(), sa.ForeignKey('tecnicos.id_tec')),
        sa.Column('estado_cot', sa.String(255)),
        sa.Column('precio_total_cot', sa.String(255)),
        sa.Column('id_equipo_cot', sa.Integer(), sa.ForeignKey('equipos.id_equ')),
        sa.Column('id_trabajo_cot', sa.Integer(), sa.ForeignKey('trabajos.id_tra')),
        sa.Column(
            'created_at_cot',
            sa.TIMESTAMP(),
            server_default=sa.text('CURRENT_TIMESTAMP'),
            nullable=False
        ),
        sa.Column(
            'updated_at_cot',
            sa.DateTime(),
            nullable=False
        ),
        sa.Column('deleted_at_cot', sa.DateTime(), nullable=True),
        sa.Column('is_deleted_cot', sa.Boolean(), server_default=sa.text('0'), nullable=False),
    )

    # ---------------- COTIZACIONES_SERVICIOS ----------------
    op.create_table(
        'cotizaciones_servicios',
        sa.Column('id_cotizacion', sa.Integer(), sa.ForeignKey('cotizaciones.id_cot'), primary_key=True),
        sa.Column('id_servicio', sa.Integer(), sa.ForeignKey('servicios.id_ser'), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table('cotizaciones_servicios')
    op.drop_table('cotizaciones')
    op.drop_table('trabajos')
    op.drop_table('equipos')
    op.drop_table('tipos_equipo')
    op.drop_table('tecnicos')
    op.drop_table('servicios')
    op.drop_table('clientes')
