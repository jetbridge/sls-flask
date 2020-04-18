"""User table

Revision ID: e1e763cb595b
Revises:
Create Date: 2020-03-20 15:26:38.847556

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "e1e763cb595b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "extid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("email", sa.Text(), nullable=True),
        sa.Column("dob", sa.Date(), nullable=True),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("phone_number", sa.Text(), nullable=True),
        sa.Column("_password", sa.Text(), nullable=True),
        sa.Column(
            "_user_type",
            sa.Enum("normal", name="usertype"),
            server_default="normal",
            nullable=False,
        ),
        sa.Column("avatar_url", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_user_extid"), "user", ["extid"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_user_extid"), table_name="user")
    op.drop_table("user")
