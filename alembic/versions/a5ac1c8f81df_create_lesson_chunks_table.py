"""create lesson_chunks table

Revision ID: a5ac1c8f81df
Revises: 
Create Date: 2026-07-27 00:18:24.532454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy


# revision identifiers, used by Alembic.
revision: str = 'a5ac1c8f81df'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table('lesson_chunks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lesson_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('chunk_order', sa.Integer(), nullable=False),
    sa.Column('embedding', pgvector.sqlalchemy.Vector(1536), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lesson_chunks_course_id'), 'lesson_chunks', ['course_id'], unique=False)
    op.create_index(op.f('ix_lesson_chunks_id'), 'lesson_chunks', ['id'], unique=False)
    op.create_index(op.f('ix_lesson_chunks_lesson_id'), 'lesson_chunks', ['lesson_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_lesson_chunks_lesson_id'), table_name='lesson_chunks')
    op.drop_index(op.f('ix_lesson_chunks_id'), table_name='lesson_chunks')
    op.drop_index(op.f('ix_lesson_chunks_course_id'), table_name='lesson_chunks')
    op.drop_table('lesson_chunks')