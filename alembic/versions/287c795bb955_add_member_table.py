"""add member table

Revision ID: 287c795bb955
Revises: 
Create Date: 2025-03-29 14:15:50.246752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '287c795bb955'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('member',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.Column('user_type', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('member')
    # ### end Alembic commands ###
