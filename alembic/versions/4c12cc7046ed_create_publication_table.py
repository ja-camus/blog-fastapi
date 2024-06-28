"""create publication table

Revision ID: 4c12cc7046ed
Revises: d590b1c01650
Create Date: 2024-06-25 15:26:04.096294

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4c12cc7046ed"
down_revision: Union[str, None] = "d590b1c01650"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "publications",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
    )

    op.create_index("ix_publications_id", "publications", ["id"], unique=False)
    op.create_index(
        "ix_publications_user_id", "publications", ["user_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_publications_user_id", table_name="publications")
    op.drop_index("ix_publications_id", table_name="publications")
    op.drop_table("publications")
