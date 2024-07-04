"""empty message

Revision ID: d7e432775171
Revises: 19a885dd3b7a
Create Date: 2024-07-04 16:48:13.593707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7e432775171'
down_revision: Union[str, None] = '19a885dd3b7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'listeners', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'listeners', type_='unique')
    # ### end Alembic commands ###