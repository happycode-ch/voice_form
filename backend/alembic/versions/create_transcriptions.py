"""create transcriptions table

Revision ID: 01
Revises: 
Create Date: 2025-05-22 18:00:43.954130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "transcriptions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_transcriptions_id"), "transcriptions", ["id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_transcriptions_id"), table_name="transcriptions")
    op.drop_table("transcriptions")
