"""Make status column not nullable

Revision ID: d4c5142d0423
Revises: 69e7ec0c4d2b
Create Date: 2025-05-06 10:57:09.316055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'd4c5142d0423'
down_revision: Union[str, None] = '69e7ec0c4d2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'status',
               existing_type=mysql.ENUM('pendiente', 'completada', 'atrasada'),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'status',
               existing_type=mysql.ENUM('pendiente', 'completada', 'atrasada'),
               nullable=True)
    # ### end Alembic commands ###
