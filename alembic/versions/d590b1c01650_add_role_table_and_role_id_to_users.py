"""Add role table and role_id to users

Revision ID: d590b1c01650
Revises: 005be9342ce0
Create Date: 2024-06-14 16:49:17.602880

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd590b1c01650'
down_revision: Union[str, None] = '005be9342ce0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(), unique=True, nullable=False),
        sa.Column("description", sa.String(), nullable=True),
    )

    op.create_index("ix_roles_id", "roles", ["id"], unique=False)
    op.create_index("ix_roles_name", "roles", ["name"], unique=True)

    op.add_column("users", sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id"), nullable=True))
    op.create_index("ix_users_role_id", "users", ["role_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_users_role_id", table_name="users")
    op.drop_column("users", "role_id")
    
    op.drop_index("ix_roles_name", table_name="roles")
    op.drop_index("ix_roles_id", table_name="roles")
    op.drop_table("roles")
