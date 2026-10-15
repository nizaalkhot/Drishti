import React, { useState } from 'react';
import { FileText, Lock, CheckCircle2, ShieldCheck, Download, Send } from 'lucide-react';
import { API_BASE } from '../config';

export default function CaseDossierModal({ caseItem, onClose, onFreeze, onSignSTR, onDismiss }) {
  const [isActing, setIsActing] = useState(false);
  const [isRecalling, setIsRecalling] = useState(false);
  const [recallResult, setRecallResult] = useState(null);

  if (!caseItem) return null;

  const tx = caseItem.transaction;
  const str = caseItem.str_report;
  const scam = caseItem.scam_decision;
  const status = caseItem.status;

  const handleDownloadFINnetXML = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/v1/cases/${caseItem.case_id}/finnet-xml`);
      if (!res.ok) throw new Error("Failed to fetch FINnet 2.0 XML");
      const xmlBlob = await res.blob();
      const url = window.URL.createObjectURL(xmlBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `FINnet2_STR_${caseItem.case_id}.xml`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (e) {
      console.error(e);
      alert("Error downloading FINnet 2.0 XML");
    }
  };

  const handleDispatchRecall = async () => {
    setIsRecalling(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/cases/${caseItem.case_id}/dispatch-recall`, {
        method: 'POST'
      });
      const data = await res.json();
      setRecallResult(data);
    } catch (e) {
      console.error(e);
      alert("Error dispatching ISO 20022 recall");
    } finally {
      setIsRecalling(false);
    }
  };

  const handleFreeze = async () => {
    setIsActing(true);
    await onFreeze(caseItem.case_id);
    setIsActing(false);
  };

  const handleSign = async () => {
    setIsActing(true);
    await onSignSTR(caseItem.case_id);
    setIsActing(false);
  };

  const handleDismiss = async () => {
    setIsActing(true);
    await onDismiss(caseItem.case_id);
    setIsActing(false);
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(5, 8, 16, 0.85)',
      backdropFilter: 'blur(16px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 200,
      padding: '24px'
    }}>
      <div className="glass-panel" style={{
        width: '900px',
        maxHeight: '90vh',
        display: 'flex',
        flexDirection: 'column',
        boxShadow: '0 25px 60px -15px rgba(0, 0, 0, 0.9)',
        border: '1px solid var(--border-active)'
      }}>
        {/* Header */}
        <div style={{
          padding: '16px 20px',
          borderBottom: '1px solid var(--border-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '8px',
              background: 'rgba(99, 102, 241, 0.2)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <FileText size={18} color="var(--accent-indigo)" />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '16px', fontWeight: 800 }}>{caseItem.case_id}</span>
                <span className={`badge ${status === 'ACCOUNT_FROZEN' ? 'badge-hold' : status === 'STR_FILED' ? 'badge-allow' : 'badge-intervene'}`}>
                  {status}
                </span>
              </div>
              <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                Transaction Ref: {tx.id} • Amount: ₹{tx.amount.toLocaleString('en-IN')}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
          >
            ✕
          </button>
        </div>

        {/* Scrollable Body */}
        <div style={{ padding: '20px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px', flex: 1 }}>
          {/* Overview Cards */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '10px' }}>
            <div style={{ background: 'rgba(255,255,255,0.02)', padding: '10px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '10px', color: 'var(--text-dim)' }}>SCAM TYPOLOGY</div>
              <div style={{ fontSize: '13px', fontWeight: 700, color: '#fb7185', marginTop: '2px' }}>
                {scam.scam_typology}
              </div>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.02)', padding: '10px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '10px', color: 'var(--text-dim)' }}>ACTIVE VOICE CALL</div>
              <div style={{ fontSize: '13px', fontWeight: 700, color: tx.device.is_call_active ? '#f59e0b' : '#94a3b8', marginTop: '2px' }}>
                {tx.device.is_call_active ? `${tx.device.call_duration_minutes.toFixed(0)} mins` : 'Inactive'}
              </div>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.02)', padding: '10px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '10px', color: 'var(--text-dim)' }}>MALICIOUS APK / MIRROR</div>
              <div style={{ fontSize: '13px', fontWeight: 700, color: (tx.device.accessibility_service_enabled || tx.device.remote_app_active) ? '#f43f5e' : '#10b981', marginTop: '2px' }}>
                {(tx.device.accessibility_service_enabled || tx.device.remote_app_active) ? 'DETECTED' : 'CLEAN'}
              </div>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.02)', padding: '10px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ fontSize: '10px', color: 'var(--text-dim)' }}>CRITIC CONFIDENCE</div>
              <div style={{ fontSize: '13px', fontWeight: 700, color: '#34d399', marginTop: '2px' }}>
                {str ? `${(str.critic_score * 100).toFixed(0)}% Validated` : 'Pending'}
              </div>
            </div>
          </div>

          {/* Grounds of Suspicion Narrative Box */}
          {str && (
            <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '14px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontSize: '11px', fontWeight: 800, color: 'var(--accent-indigo)', letterSpacing: '0.05em' }}>
                  FIU-IND COMPLIANT STR DRAFT (PMLA 2002)
                </span>
                <span style={{ fontSize: '10px', color: 'var(--text-dim)' }}>
                  Ref: {str.str_reference_no}
                </span>
              </div>
              <pre style={{
                whiteSpace: 'pre-wrap',
                fontFamily: 'monospace',
                fontSize: '11px',
                color: '#cbd5e1',
                lineHeight: 1.5,
                background: 'rgba(0,0,0,0.3)',
                padding: '12px',
                borderRadius: '6px'
              }}>
                {str.grounds_of_suspicion}
              </pre>
            </div>
          )}

          {/* Verified Evidence Citations */}
          {str && str.verified_evidence_citations && str.verified_evidence_citations.length > 0 && (
            <div>
              <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-dim)', marginBottom: '6px', textTransform: 'uppercase' }}>
                VERIFIED REGULATORY, CONSORTIUM & TELEMETRY CITATIONS
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                {str.verified_evidence_citations.map((cite, i) => (
                  <div key={i} style={{ fontSize: '11px', color: '#94a3b8', display: 'flex', alignItems: 'flex-start', gap: '6px' }}>
                    <span style={{ color: 'var(--accent-indigo)' }}>•</span> {cite}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* CON 4: Principal Officer Verification Checklist & Digital Sign-off */}
          {str && (
            <div style={{
              background: 'rgba(99, 102, 241, 0.08)',
              padding: '12px',
              borderRadius: '8px',
              border: '1px solid rgba(99, 102, 241, 0.25)',
              display: 'flex',
              flexDirection: 'column',
              gap: '8px'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ fontSize: '11px', fontWeight: 800, color: '#a5b4fc', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <ShieldCheck size={16} /> PRINCIPAL OFFICER VERIFICATION GATE (PMLA SEC 12)
                </span>
                <span style={{
                  fontSize: '10px',
                  fontWeight: 700,
                  color: str.human_sign_off_status === 'APPROVED_DIGITALLY_SIGNED' ? '#34d399' : '#fbbf24',
                  background: str.human_sign_off_status === 'APPROVED_DIGITALLY_SIGNED' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                  padding: '2px 8px',
                  borderRadius: '12px'
                }}>
                  {str.human_sign_off_status}
                </span>
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '11px', color: '#cbd5e1' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span className="badge badge-allow font-mono" style={{ fontSize: '9px', padding: '1px 5px' }}>VERIFIED</span>
                  <span>Beneficiary KYC Profile Inspected</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span className="badge badge-allow font-mono" style={{ fontSize: '9px', padding: '1px 5px' }}>VERIFIED</span>
                  <span>PMLA Sec 12 Regulatory Alignment</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span className="badge badge-allow font-mono" style={{ fontSize: '9px', padding: '1px 5px' }}>VERIFIED</span>
                  <span>Telephony & Network Citations Validated</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span className="badge badge-allow font-mono" style={{ fontSize: '9px', padding: '1px 5px' }}>VERIFIED</span>
                  <span>I4C / NPCI Registry Cross-Check Complete</span>
                </div>
              </div>
              {str.po_signature_hash && (
                <div style={{ fontSize: '10px', color: '#94a3b8', background: 'rgba(0,0,0,0.3)', padding: '6px', borderRadius: '4px' }}>
                  <strong>Digital Signature Hash:</strong> <code>{str.po_signature_hash}</code><br />
                  <strong>Signed By:</strong> {str.signed_by}
                </div>
              )}
            </div>
          )}

          {/* ISO 20022 Recall Acknowledgement Banner */}
          {recallResult && (
            <div style={{
              marginTop: '12px',
              padding: '12px 14px',
              borderRadius: '10px',
              background: 'rgba(16, 185, 129, 0.12)',
              border: '1px solid rgba(16, 185, 129, 0.35)',
              display: 'flex',
              flexDirection: 'column',
              gap: '4px'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ fontSize: '11px', fontWeight: 800, color: '#34d399' }} className="font-mono">
                  ISO 20022 CLAWBACK DISPATCHED ({recallResult.standard})
                </span>
                <span className="badge badge-allow font-mono" style={{ fontSize: '9px' }}>
                  {recallResult.interbank_acknowledgement}
                </span>
              </div>
              <div style={{ fontSize: '11px', color: '#cbd5e1' }}>
                Demanded immediate interbank freeze of ₹{recallResult.clawback_amount_inr.toLocaleString('en-IN')} on beneficiary <strong>{recallResult.target_beneficiary_vpa}</strong> at receiving bank ({recallResult.instructed_agent}).
              </div>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div style={{
          padding: '14px 20px',
          borderTop: '1px solid var(--border-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'rgba(8, 12, 20, 0.6)',
          flexWrap: 'wrap',
          gap: '8px'
        }}>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <button
              onClick={handleFreeze}
              disabled={isActing || status === 'ACCOUNT_FROZEN'}
              className="btn btn-danger"
              style={{ fontSize: '12px', padding: '8px 12px' }}
            >
              <Lock size={13} /> Mark Lien & Freeze Account
            </button>

            <button
              onClick={handleDispatchRecall}
              disabled={isRecalling || recallResult !== null}
              className="btn btn-primary"
              style={{
                fontSize: '12px',
                padding: '8px 12px',
                background: recallResult ? 'rgba(16, 185, 129, 0.2)' : 'linear-gradient(135deg, #0284c7 0%, #0369a1 100%)',
                border: recallResult ? '1px solid #10b981' : '1px solid rgba(255,255,255,0.2)'
              }}
            >
              <Send size={13} /> {isRecalling ? 'Dispatching...' : recallResult ? 'ISO Recall Active' : 'Dispatch ISO 20022 Recall'}
            </button>

            <button
              onClick={handleSign}
              disabled={isActing || status === 'STR_FILED'}
              className="btn btn-primary"
              style={{ fontSize: '12px', padding: '8px 12px' }}
            >
              <CheckCircle2 size={13} /> Sign STR
            </button>

            <button
              onClick={handleDownloadFINnetXML}
              className="btn btn-outline"
              style={{ fontSize: '12px', padding: '8px 12px', color: '#67e8f9', borderColor: 'rgba(6, 182, 212, 0.4)' }}
            >
              <Download size={13} /> FINnet 2.0 XML
            </button>
          </div>

          <button
            onClick={handleDismiss}
            disabled={isActing || status === 'FALSE_POSITIVE_DISMISSED'}
            className="btn btn-outline"
            style={{ fontSize: '12px', padding: '8px 12px' }}
          >
            Dismiss
          </button>
        </div>
      </div>
    </div>
  );
}
