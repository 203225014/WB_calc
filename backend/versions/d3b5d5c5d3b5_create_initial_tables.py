"""Create initial tables

Revision ID: d3b5d5c5d3b5
Revises: 
Create Date: 2025-11-04 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd3b5d5c5d3b5'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create calculations table
    op.create_table(
        'calculations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('purchase_price', sa.Float(), nullable=False),
        sa.Column('desired_profit', sa.Float(), nullable=False),
        sa.Column('length', sa.Float(), nullable=False),
        sa.Column('width', sa.Float(), nullable=False),
        sa.Column('height', sa.Float(), nullable=False),
        sa.Column('commission_wb_percent', sa.Float(), nullable=False),
        sa.Column('acquiring_percent', sa.Float(), nullable=False),
        sa.Column('tax_percent', sa.Float(), nullable=False),
        sa.Column('ads_percent', sa.Float(), nullable=False),
        sa.Column('logistics_coefficient', sa.Float(), nullable=False),
        sa.Column('return_cost', sa.Float(), nullable=False),
        sa.Column('buyout_percent', sa.Float(), nullable=False),
        sa.Column('storage_cost', sa.Float(), nullable=False),
        sa.Column('volume_liters', sa.Float(), nullable=False),
        sa.Column('logistics_cost', sa.Float(), nullable=False),
        sa.Column('total_logistics_cost', sa.Float(), nullable=False),
        sa.Column('client_price', sa.Float(), nullable=False),
        sa.Column('ads_cost', sa.Float(), nullable=False),
        sa.Column('commission_wb_cost', sa.Float(), nullable=False),
        sa.Column('acquiring_cost', sa.Float(), nullable=False),
        sa.Column('tax_cost', sa.Float(), nullable=False),
        sa.Column('storage_cost_result', sa.Float(), nullable=False),
        sa.Column('final_cost', sa.Float(), nullable=False),
        sa.Column('profit_per_unit', sa.Float(), nullable=False),
        sa.Column('margin_percent', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('calculations')
    op.drop_table('users')