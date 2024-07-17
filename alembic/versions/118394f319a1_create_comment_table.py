"""create comment table

Revision ID: 118394f319a1
Revises: 4c12cc7046ed
Create Date: 2024-07-03 14:52:44.169910

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "118394f319a1"
down_revision: Union[str, None] = "4c12cc7046ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "publication_id",
            sa.Integer(),
            sa.ForeignKey("publications.id"),
            nullable=False,
        ),
    )
    op.create_index("ix_comments_id", "comments", ["id"], unique=False)
    op.create_index("ix_comments_user_id", "comments", ["user_id"], unique=False)
    op.create_index(
        "ix_comments_publication_id", "comments", ["publication_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_comments_publication_id", table_name="comments")
    op.drop_index("ix_comments_user_id", table_name="comments")
    op.drop_index("ix_comments_id", table_name="comments")
    op.drop_table("comments")
