"""0001_initial_schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-10-16 22:40:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # case_dossiers
    op.create_table(
        'case_dossiers',
        sa.Column('case_id', sa.String(length=64), primary_key=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('transaction_id', sa.String(length=64), nullable=True),
        sa.Column('sender_vpa', sa.String(length=128), nullable=True),
        sa.Column('receiver_vpa', sa.String(length=128), nullable=True),
        sa.Column('amount', sa.Float(), nullable=True),
        sa.Column('risk_score', sa.Float(), nullable=True),
        sa.Column('decision', sa.String(length=32), nullable=True),
        sa.Column('scam_typology', sa.String(length=64), nullable=True),
        sa.Column('is_synthetic', sa.Boolean(), nullable=True, default=False),
        sa.Column('environment', sa.String(length=32), nullable=True, default="production"),
        sa.Column('transaction_json', sa.JSON(), nullable=True),
        sa.Column('features_json', sa.JSON(), nullable=True),
        sa.Column('risk_result_json', sa.JSON(), nullable=True),
        sa.Column('scam_decision_json', sa.JSON(), nullable=True),
        sa.Column('str_report_json', sa.JSON(), nullable=True),
        sa.Column('investigator_notes', sa.Text(), nullable=True),
        sa.Column('audit_history_json', sa.JSON(), nullable=True),
    )
    op.create_index('ix_case_dossiers_case_id', 'case_dossiers', ['case_id'])
    op.create_index('ix_case_dossiers_created_at', 'case_dossiers', ['created_at'])
    op.create_index('ix_case_dossiers_status', 'case_dossiers', ['status'])
    op.create_index('ix_case_dossiers_is_synthetic', 'case_dossiers', ['is_synthetic'])

    # consent_receipts
    op.create_table(
        'consent_receipts',
        sa.Column('receipt_id', sa.String(length=64), primary_key=True),
        sa.Column('transaction_id', sa.String(length=64), nullable=True),
        sa.Column('customer_id', sa.String(length=64), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('scam_score', sa.Float(), nullable=True),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('chain_hash', sa.String(length=64), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('can_proceed', sa.Boolean(), nullable=True),
        sa.Column('raw_request_json', sa.JSON(), nullable=True),
    )
    op.create_index('ix_consent_receipts_receipt_id', 'consent_receipts', ['receipt_id'])
    op.create_index('ix_consent_receipts_transaction_id', 'consent_receipts', ['transaction_id'])
    op.create_index('ix_consent_receipts_chain_hash', 'consent_receipts', ['chain_hash'])

    # audit_logs
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('case_id', sa.String(length=64), nullable=True),
        sa.Column('action', sa.String(length=64), nullable=True),
        sa.Column('actor', sa.String(length=128), nullable=True),
        sa.Column('details_json', sa.JSON(), nullable=True),
    )
    op.create_index('ix_audit_logs_timestamp', 'audit_logs', ['timestamp'])
    op.create_index('ix_audit_logs_action', 'audit_logs', ['action'])

def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('consent_receipts')
    op.drop_table('case_dossiers')
