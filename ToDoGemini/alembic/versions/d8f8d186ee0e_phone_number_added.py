"""phone number added

Revision ID: d8f8d186ee0e
Revises: 
Create Date: 2025-03-10 17:04:09.666897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8f8d186ee0e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.String,nullable=True))



def downgrade() -> None:
    pass
