"""Добавлен констрейн уникального title для зала

Revision ID: 5744a17f2cc3
Revises: a5a017b79814
Create Date: 2024-12-08 14:46:01.419541

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5744a17f2cc3'
down_revision: Union[str, None] = 'a5a017b79814'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'halls', ['title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'halls', type_='unique')
    # ### end Alembic commands ###
