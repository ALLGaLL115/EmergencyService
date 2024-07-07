"""empty message

Revision ID: 2b5c2f0b691c
Revises: 
Create Date: 2024-07-05 22:22:23.436771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b5c2f0b691c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('listeners',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone', sa.String(length=18), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=128), nullable=True),
    sa.Column('time_updated', sa.DateTime(), nullable=True),
    sa.Column('time_created', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('listeners_notifications',
    sa.Column('listener_id', sa.Integer(), nullable=False),
    sa.Column('notification_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['listener_id'], ['listeners.id'], ),
    sa.ForeignKeyConstraint(['notification_id'], ['notifications.id'], ),
    sa.PrimaryKeyConstraint('listener_id', 'notification_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('listeners_notifications')
    op.drop_table('notifications')
    op.drop_table('listeners')
    # ### end Alembic commands ###