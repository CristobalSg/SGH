"""update_seccion_add_anio_academico_tipo_grupo_numero_estudiantes

Revision ID: 3dc2453812ae
Revises: c7d8e9f0a1b2
Create Date: 2025-11-19 13:23:59.765086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3dc2453812ae'
down_revision: Union[str, Sequence[str], None] = 'c7d8e9f0a1b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Verificar y agregar columnas a asignatura solo si no existen
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    asignatura_columns = [col['name'] for col in inspector.get_columns('asignatura')]
    
    if 'horas_presenciales' not in asignatura_columns:
        op.add_column('asignatura', sa.Column('horas_presenciales', sa.Integer(), nullable=False, server_default='0'))
    if 'horas_mixtas' not in asignatura_columns:
        op.add_column('asignatura', sa.Column('horas_mixtas', sa.Integer(), nullable=False, server_default='0'))
    if 'horas_autonomas' not in asignatura_columns:
        op.add_column('asignatura', sa.Column('horas_autonomas', sa.Integer(), nullable=False, server_default='0'))
    if 'cantidad_creditos' not in asignatura_columns:
        op.add_column('asignatura', sa.Column('cantidad_creditos', sa.Integer(), nullable=False, server_default='0'))
    if 'semestre' not in asignatura_columns:
        op.add_column('asignatura', sa.Column('semestre', sa.Integer(), nullable=False, server_default='1'))
    
    # Migrar creditos a cantidad_creditos si la columna creditos existe
    if 'creditos' in asignatura_columns:
        op.execute("UPDATE asignatura SET cantidad_creditos = COALESCE(creditos, 0)")
        op.drop_column('asignatura', 'creditos')
    
    # Remover server_default después de migrar
    op.alter_column('asignatura', 'horas_presenciales', server_default=None)
    op.alter_column('asignatura', 'horas_mixtas', server_default=None)
    op.alter_column('asignatura', 'horas_autonomas', server_default=None)
    op.alter_column('asignatura', 'cantidad_creditos', server_default=None)
    op.alter_column('asignatura', 'semestre', server_default=None)
    
    # Actualizar foreign keys de docente
    op.alter_column('clase', 'docente_id', existing_type=sa.INTEGER(), nullable=False)
    op.drop_constraint('clase_docente_id_fkey', 'clase', type_='foreignkey')
    op.create_foreign_key('clase_docente_id_fkey', 'clase', 'docente', ['docente_id'], ['user_id'])
    
    op.drop_index('ix_evento_activo', table_name='evento', if_exists=True)
    op.drop_index('ix_evento_clase_id', table_name='evento', if_exists=True)
    op.drop_index('ix_evento_created_at', table_name='evento', if_exists=True)
    op.drop_index('ix_evento_docente_id', table_name='evento', if_exists=True)
    op.drop_constraint('evento_docente_id_fkey', 'evento', type_='foreignkey')
    op.create_foreign_key('evento_docente_id_fkey', 'evento', 'docente', ['docente_id'], ['user_id'])
    
    op.alter_column('restriccion', 'docente_id', existing_type=sa.INTEGER(), nullable=False)
    op.drop_constraint('restriccion_docente_id_fkey', 'restriccion', type_='foreignkey')
    op.create_foreign_key('restriccion_docente_id_fkey', 'restriccion', 'docente', ['docente_id'], ['user_id'])
    
    op.alter_column('restriccion_horario', 'docente_id', existing_type=sa.INTEGER(), nullable=False)
    op.drop_constraint('restriccion_horario_docente_id_fkey', 'restriccion_horario', type_='foreignkey')
    op.create_foreign_key('restriccion_horario_docente_id_fkey', 'restriccion_horario', 'docente', ['docente_id'], ['user_id'])
    
    # Verificar y agregar columnas a seccion solo si no existen
    seccion_columns = [col['name'] for col in inspector.get_columns('seccion')]
    
    if 'anio_academico' not in seccion_columns:
        op.add_column('seccion', sa.Column('anio_academico', sa.Integer(), nullable=True))
    if 'tipo_grupo' not in seccion_columns:
        op.add_column('seccion', sa.Column('tipo_grupo', sa.String(length=20), nullable=True))
    if 'numero_estudiantes' not in seccion_columns:
        op.add_column('seccion', sa.Column('numero_estudiantes', sa.Integer(), nullable=True))
    
    # Migrar datos existentes
    if 'anio' in seccion_columns:
        op.execute("UPDATE seccion SET anio_academico = COALESCE(anio, 1) WHERE anio_academico IS NULL")
    op.execute("UPDATE seccion SET tipo_grupo = 'seccion' WHERE tipo_grupo IS NULL")
    op.execute("UPDATE seccion SET numero_estudiantes = COALESCE(cupos, 30) WHERE numero_estudiantes IS NULL")
    
    # Hacer NOT NULL después de migrar
    op.alter_column('seccion', 'anio_academico', nullable=False)
    op.alter_column('seccion', 'tipo_grupo', nullable=False)
    op.alter_column('seccion', 'numero_estudiantes', nullable=False)
    
    # Eliminar columna anio si existe
    if 'anio' in seccion_columns:
        op.drop_column('seccion', 'anio')


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    seccion_columns = [col['name'] for col in inspector.get_columns('seccion')]
    
    if 'anio' not in seccion_columns:
        op.add_column('seccion', sa.Column('anio', sa.INTEGER(), autoincrement=False, nullable=True))
    if 'numero_estudiantes' in seccion_columns:
        op.drop_column('seccion', 'numero_estudiantes')
    if 'tipo_grupo' in seccion_columns:
        op.drop_column('seccion', 'tipo_grupo')
    if 'anio_academico' in seccion_columns:
        op.drop_column('seccion', 'anio_academico')
    
    op.drop_constraint('restriccion_horario_docente_id_fkey', 'restriccion_horario', type_='foreignkey')
    op.create_foreign_key('restriccion_horario_docente_id_fkey', 'restriccion_horario', 'docente', ['docente_id'], ['user_id'], ondelete='CASCADE')
    op.alter_column('restriccion_horario', 'docente_id', existing_type=sa.INTEGER(), nullable=True)
    
    op.drop_constraint('restriccion_docente_id_fkey', 'restriccion', type_='foreignkey')
    op.create_foreign_key('restriccion_docente_id_fkey', 'restriccion', 'docente', ['docente_id'], ['user_id'], ondelete='CASCADE')
    op.alter_column('restriccion', 'docente_id', existing_type=sa.INTEGER(), nullable=True)
    
    op.drop_constraint('evento_docente_id_fkey', 'evento', type_='foreignkey')
    op.create_foreign_key('evento_docente_id_fkey', 'evento', 'docente', ['docente_id'], ['user_id'], ondelete='CASCADE')
    op.create_index('ix_evento_docente_id', 'evento', ['docente_id'], unique=False)
    op.create_index('ix_evento_created_at', 'evento', ['created_at'], unique=False)
    op.create_index('ix_evento_clase_id', 'evento', ['clase_id'], unique=False)
    op.create_index('ix_evento_activo', 'evento', ['activo'], unique=False)
    
    op.drop_constraint('clase_docente_id_fkey', 'clase', type_='foreignkey')
    op.create_foreign_key('clase_docente_id_fkey', 'clase', 'docente', ['docente_id'], ['user_id'], ondelete='CASCADE')
    op.alter_column('clase', 'docente_id', existing_type=sa.INTEGER(), nullable=True)
    
    asignatura_columns = [col['name'] for col in inspector.get_columns('asignatura')]
    if 'creditos' not in asignatura_columns:
        op.add_column('asignatura', sa.Column('creditos', sa.INTEGER(), autoincrement=False, nullable=True))
    if 'semestre' in asignatura_columns:
        op.drop_column('asignatura', 'semestre')
    if 'cantidad_creditos' in asignatura_columns:
        op.drop_column('asignatura', 'cantidad_creditos')
    if 'horas_autonomas' in asignatura_columns:
        op.drop_column('asignatura', 'horas_autonomas')
    if 'horas_mixtas' in asignatura_columns:
        op.drop_column('asignatura', 'horas_mixtas')
    if 'horas_presenciales' in asignatura_columns:
        op.drop_column('asignatura', 'horas_presenciales')
