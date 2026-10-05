import React from 'react';
import { ShieldCheck } from 'lucide-react';

export default function ConsentAuditModal({
  confirmedNoCoercion,
  setConfirmedNoCoercion,
  consentReceipt,
  isSubmittingConsent,
  onRecordConsent,
  onCancel
}) {
  return (
    <div style={{
      background: 'rgba(15, 23, 42, 0.9)',
      padding: '12px',
      borderRadius: '10px',
      border: '1px solid rgba(99, 102, 241, 0.4)',
      display: 'flex',
      flexDirection: 'column',
      gap: '8px'
    }}>
      <div style={{ fontSize: '11px', fontWeight: 800, color: '#a5b4fc', display: 'flex', alignItems: 'center', gap: '6px' }}>
        <ShieldCheck size={16} />
        Informed Consent Audit Vault
      </div>
      <label style={{ fontSize: '10px', color: '#cbd5e1', display: 'flex', gap: '6px', cursor: 'pointer' }}>
        <input
          type="checkbox"
          checked={confirmedNoCoercion}
          onChange={(e) => setConfirmedNoCoercion(e.target.checked)}
        />
        <span>I certify I am NOT sending funds under direction of police, CBI, or unknown callers.</span>
      </label>

      {consentReceipt && (
        <div style={{
          padding: '6px 8px',
          borderRadius: '6px',
          background: consentReceipt.can_proceed ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)',
          border: '1px solid rgba(255,255,255,0.1)',
          fontSize: '9px',
          color: consentReceipt.can_proceed ? '#34d399' : '#f87171'
        }}>
          <strong>Receipt:</strong> {consentReceipt.receipt_id}<br />
          <strong>Chain Hash:</strong> {consentReceipt.chain_hash?.slice(0, 16)}...<br />
          {consentReceipt.reason}
        </div>
      )}

      <div style={{ display: 'flex', gap: '6px', marginTop: '4px' }}>
        <button
          type="button"
          onClick={onRecordConsent}
          disabled={!confirmedNoCoercion || isSubmittingConsent}
          className="btn btn-primary"
          style={{ flex: 1, padding: '8px', fontSize: '11px' }}
        >
          {isSubmittingConsent ? 'Signing Ledger...' : 'Sign with Biometric PIN'}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="btn btn-outline"
          style={{ padding: '8px 12px', fontSize: '11px' }}
        >
          Back
        </button>
      </div>
    </div>
  );
}
