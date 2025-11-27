"""add_all_missing_schema_elements

Revision ID: e785a3a7c71b
Revises: 0280051d178a
Create Date: 2025-11-27 02:24:38.699867

Comprehensive fix for all missing schema elements found by auditing storage code:
1. Add datatype_name_text_id to custom_datatypes table
2. Add config_xsi_type to device_test_config table
3. Create missing std_variable_ref_value_ranges table
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e785a3a7c71b'
down_revision = '0280051d178a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add all missing schema elements"""

    # 1. Add datatype_name_text_id to custom_datatypes table
    with op.batch_alter_table('custom_datatypes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('datatype_name_text_id', sa.VARCHAR(255), nullable=True))

    # 2. Add config_xsi_type to device_test_config table
    with op.batch_alter_table('device_test_config', schema=None) as batch_op:
        batch_op.add_column(sa.Column('config_xsi_type', sa.VARCHAR(100), nullable=True))

    # 3. Create std_variable_ref_value_ranges table
    op.create_table(
        'std_variable_ref_value_ranges',
        sa.Column('id', sa.INTEGER, primary_key=True, autoincrement=True),
        sa.Column('std_variable_ref_id', sa.INTEGER, nullable=False),
        sa.Column('lower_value', sa.TEXT, nullable=True),
        sa.Column('upper_value', sa.TEXT, nullable=True),
        sa.Column('is_std_ref', sa.INTEGER, nullable=False),
        sa.Column('order_index', sa.INTEGER, nullable=True),
        sa.ForeignKeyConstraint(['std_variable_ref_id'], ['std_variable_refs.id'], ondelete='CASCADE')
    )


def downgrade() -> None:
    """Remove all added schema elements"""

    # Drop table
    op.drop_table('std_variable_ref_value_ranges')

    # Drop columns
    with op.batch_alter_table('device_test_config', schema=None) as batch_op:
        batch_op.drop_column('config_xsi_type')

    with op.batch_alter_table('custom_datatypes', schema=None) as batch_op:
        batch_op.drop_column('datatype_name_text_id')
