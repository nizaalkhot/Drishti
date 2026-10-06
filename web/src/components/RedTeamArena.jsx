import React, { useState } from 'react';
import { Bug, ShieldAlert, Play, ShieldCheck } from 'lucide-react';
import { API_BASE } from '../config';

export default function RedTeamArena() {
  const [archetype, setArchetype] = useState('OBFUSCATED_REMARK');
  const [isProbing, setIsProbing] = useState(false);
  const [report, setReport] = useState(null);

  const handleProbe = async () => {
    setIsProbing(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/redteam/probe`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ archetype })
      });
      const data = await res.json();
      setReport(data);
    } catch (e) {
      console.error(e);
      alert(`Failed to connect to backend red-team service at ${API_BASE}`);
    } finally {
      setIsProbing(false);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '38px',
            height: '38px',
            borderRadius: '10px',
            background: 'rgba(239, 68, 68, 0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '1px solid rgba(239, 68, 68, 0.35)',
            boxShadow: '0 0 16px rgba(239, 68, 68, 0.2)'
          }}>
            <Bug size={20} color="#ef4444" />
          </div>
          <div>
            <h2 style={{ fontSize: '18px', fontWeight: 800, color: '#f8fafc' }} className="font-display">
              Adversarial Red-Team Arena
            </h2>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Self-Play Attack Vectors • Continuous Defense Gap Discovery & Remediation
            </p>
          </div>
        </div>

        <span className="badge badge-hold" style={{ fontSize: '11px', padding: '5px 12px' }}>
          OFFLINE STRESS-TEST ENGINE
        </span>
      </div>

      {/* Attack Selection Panel */}
      <div style={{ background: 'rgba(255,255,255,0.02)', padding: '18px', borderRadius: '14px', border: '1px solid var(--border-subtle)', marginBottom: '20px' }}>
        <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-dim)', marginBottom: '12px', letterSpacing: '0.04em' }} className="font-mono">
          SELECT ADVERSARIAL ATTACK ARCHETYPE
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '14px' }}>
          {[
            {
              id: 'OBFUSCATED_REMARK',
              title: 'Obfuscated Remark Injection',
              desc: 'Leetspeak & Unicode padding (e.g. "F@mily m3dical cl3arance") to evade keyword filters.'
            },
            {
              id: 'STRUCTURED_SMURFING',
              title: 'Structured Smurfing (<₹50k)',
              desc: 'Transactions structured at ₹49,900 to slip below statutory PAN reporting limits.'
            },
            {
              id: 'DEEPFAKE_AUTHORITY',
              title: 'Deepfake Judicial Authority',
              desc: 'Impersonating judicial officers using polite, non-banned regulatory vocabulary.'
            }
          ].map((item) => {
            const isSelected = archetype === item.id;
            return (
              <div
                key={item.id}
                onClick={() => setArchetype(item.id)}
                className="interactive-card"
                style={{
                  padding: '14px',
                  borderRadius: '10px',
                  background: isSelected ? 'rgba(239, 68, 68, 0.12)' : 'rgba(255,255,255,0.02)',
                  border: isSelected ? '1px solid #ef4444' : '1px solid var(--border-subtle)',
                  cursor: 'pointer',
                  boxShadow: isSelected ? '0 0 16px rgba(239, 68, 68, 0.25)' : 'none'
                }}
              >
                <div style={{ fontSize: '13px', fontWeight: 700, color: isSelected ? '#ffffff' : '#cbd5e1' }} className="font-display">
                  {item.title}
                </div>
                <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '6px', lineHeight: 1.45 }}>
                  {item.desc}
                </p>
              </div>
            );
          })}
        </div>

        <button
          onClick={handleProbe}
          disabled={isProbing}
          className="btn btn-danger"
          style={{ marginTop: '16px', padding: '10px 22px', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '8px' }}
        >
          <Play size={14} fill="#ffffff" />
          {isProbing ? 'Simulating Attack Vector...' : 'Launch Adversarial Probe against Drishti'}
        </button>
      </div>

      {/* Probe Result & Defense Gap Report */}
      {report && (
        <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Evasion Banner */}
          <div style={{
            padding: '16px 20px',
            borderRadius: '12px',
            background: report.evasion_successful ? 'rgba(239, 68, 68, 0.14)' : 'rgba(16, 185, 129, 0.14)',
            border: `1px solid ${report.evasion_successful ? '#ef4444' : '#10b981'}`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            boxShadow: report.evasion_successful ? '0 0 20px rgba(239, 68, 68, 0.2)' : '0 0 20px rgba(16, 185, 129, 0.2)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              {report.evasion_successful ? <ShieldAlert size={26} color="#ef4444" /> : <ShieldCheck size={26} color="#10b981" />}
              <div>
                <div style={{ fontSize: '15px', fontWeight: 800, color: report.evasion_successful ? '#fca5a5' : '#34d399' }} className="font-display">
                  {report.evasion_successful ? 'VULNERABILITY CONFIRMED: Defense Evaded' : 'PROBE INTERCEPTED: Defenses Held Firm'}
                </div>
                <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }} className="font-mono tabular-nums">
                  Layer 1 Score: {report.layer1_score} • Decision: {report.layer1_decision} • Scam Shield: {report.scam_detected ? 'Intercepted' : 'Bypassed'}
                </div>
              </div>
            </div>

            <span className={`badge ${report.evasion_successful ? 'badge-hold' : 'badge-allow'}`}>
              {report.evasion_successful ? 'GAP DETECTED' : 'SECURE'}
            </span>
          </div>

          {/* Defense Gap Analysis */}
          <div style={{ background: 'rgba(15, 23, 42, 0.7)', padding: '18px 20px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
            <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#f8fafc', marginBottom: '6px' }} className="font-display">
              Vulnerability Analysis
            </h4>
            <p style={{ fontSize: '12px', color: '#cbd5e1', lineHeight: 1.5 }}>
              {report.vulnerability_found}
            </p>

            <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#38bdf8', marginTop: '16px', marginBottom: '6px' }} className="font-display">
              Recommended Remediation Policy
            </h4>
            <p style={{ fontSize: '12px', color: '#cbd5e1', lineHeight: 1.5 }}>
              {report.remediation_rule}
            </p>

            <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#34d399', marginTop: '16px', marginBottom: '8px' }} className="font-display">
              Automated Defense Patch
            </h4>
            <pre style={{
              background: 'rgba(0,0,0,0.45)',
              padding: '12px 16px',
              borderRadius: '8px',
              fontSize: '11px',
              color: '#a7f3d0',
              overflowX: 'auto',
              border: '1px solid rgba(255, 255, 255, 0.08)'
            }} className="font-mono">
              {report.recommended_patch}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
