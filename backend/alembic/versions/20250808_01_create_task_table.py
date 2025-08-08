from alembic import op
import sqlalchemy as sa

revision = '20250808_01'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'task',
        sa.Column('id', sa.String(), primary_key=True, index=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, default='todo'),
        sa.Column('priority', sa.String(), nullable=False, default='medium'),
        sa.Column('dueDate', sa.DateTime(), nullable=True),
        sa.Column('createdAt', sa.DateTime(), nullable=False),
        sa.Column('updatedAt', sa.DateTime(), nullable=False),
    )

def downgrade():
    op.drop_table('task')
