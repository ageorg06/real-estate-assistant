from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'property_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('lead_id', sa.String(), nullable=False),
        sa.Column('transaction_type', sa.String(), nullable=True),
        sa.Column('property_type', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('min_price', sa.Float(), nullable=True),
        sa.Column('max_price', sa.Float(), nullable=True),
        sa.Column('min_bedrooms', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_property_preferences_lead_id', 'property_preferences', ['lead_id'])

def downgrade():
    op.drop_table('property_preferences')