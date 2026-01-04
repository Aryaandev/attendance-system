"""add user approval status

Revision ID: 2b5fe60294a9
Revises: a759b4770649
Create Date: 2025-12-22 03:56:42.135644
"""

from alembic import op
import sqlalchemy as sa


revision = '2b5fe60294a9'
down_revision = 'a759b4770649'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('user_id', sa.String(length=50), nullable=True)
        )
        batch_op.add_column(
            sa.Column('status', sa.String(length=20), nullable=True, server_default="pending")
        )

        batch_op.alter_column(
            'email',
            existing_type=sa.VARCHAR(length=120),
            nullable=True
        )
        batch_op.alter_column(
            'password_hash',
            existing_type=sa.VARCHAR(length=255),
            nullable=True
        )

        # ✅ NAMED UNIQUE CONSTRAINT (FIX)
        batch_op.create_unique_constraint(
            "uq_user_user_id",
            ["user_id"]
        )


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        # ✅ DROP BY NAME
        batch_op.drop_constraint(
            "uq_user_user_id",
            type_="unique"
        )

        batch_op.alter_column(
            'password_hash',
            existing_type=sa.VARCHAR(length=255),
            nullable=False
        )
        batch_op.alter_column(
            'email',
            existing_type=sa.VARCHAR(length=120),
            nullable=False
        )

        batch_op.drop_column('status')
        batch_op.drop_column('user_id')
