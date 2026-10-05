import React, { useState } from 'react';
import { Bug, ShieldAlert, CheckCircle2, AlertTriangle, ArrowRight, Terminal, RefreshCw, Cpu } from 'lucide-react';

export default function RedTeamArena() {
  const [archetype, setArchetype] = useState('OBFUSCATED_REMARK');
  const [isProbing, setIsProbing] = useState(false);
  const [report, setReport] = useState(null);

  const handleProbe = async () => {
    setIsProbing(true);
    try {
      const res = await fetch('http://localhost:8000/api/v1/redteam/probe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ archetype })
      });
      const data = await res.json();
      setReport(data);
    } catch (e) {
      console.error(e);
      alert("Failed to connect to backend red-team service at http://localhost:8000");
    } finally {
      setIsProbing(false);
    }
  };

  return (
    <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '10px',
            background: 'rgba(244, 63, 94, 0.2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '1px solid rgba(244, 63, 94, 0.4)'
          }}>
            <Bug size={20} color="#f43f5e" />
          </div>
          <div>
            <h2 style={{ fontSize: '18px', fontWeight: 800 }}>Adversarial Red-Team Arena</h2>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Self-Play Attack Vectors • Continuous Defense Gap Discovery & Remediation
            </p>
          </div>
        </div>

        <span className="badge badge-hold">
          OFFLINE STRESS-TEST ENGINE
        </span>
      </div>

      {/* Attack Selection Panel */}
      <div style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-subtle)', marginBottom: '20px' }}>
        <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-dim)', marginBottom: '10px', textTransform: 'uppercase' }}>
          SELECT ADVERSARIAL ATTACK ARCHETYPE
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px' }}>
          {[
            {
              id: 'OBFUSCATED_REMARK',
              title: 'Obfuscated Remark Injection',
              desc: 'Leetspeak & Unicode padding (e.g. "F@mily m3dical cl3arance") to evade keyword filters.'
            },
            {
              id: 'STRUCTURED_SMURFING',
              title: 'Structured Smurfing (&lt;₹50k)',
              desc: 'Transactions structured at ₹49,900 to slip below statutory PAN reporting limits.'
            },
            {
              id: 'DEEPFAKE_AUTHORITY',
              title: 'Deepfake Judicial Authority',
              desc: 'Impersonating judicial officers using polite, non-banned regulatory vocabulary.'
            }
          ].map((item) => (
            <div
              key={item.id}
              onClick={() => setArchetype(item.id)}
              style={{
                padding: '12px',
                borderRadius: '8px',
                background: archetype === item.id ? 'rgba(244, 63, 94, 0.15)' : 'rgba(255,255,255,0.02)',
                border: archetype === item.id ? '1px solid #f43f5e' : '1px solid var(--border-subtle)',
                cursor: 'pointer',
                transition: 'all 0.15s ease'
              }}
            >
              <div style={{ fontSize: '13px', fontWeight: 700, color: archetype === item.id ? '#ffffff' : '#cbd5e1' }}>
                {item.title}
              </div>
              <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px', lineHeight: 1.4 }}>
                {item.desc}
              </p>
            </div>
          ))}
        </div>

        <button
          onClick={handleProbe}
          disabled={isProbing}
          className="btn btn-danger"
          style={{ marginTop: '16px', padding: '10px 20px', fontSize: '13px' }}
        >
          {isProbing ? 'Simulating Attack Vector...' : 'Launch Adversarial Probe against Drishti'}
        </button>
      </div>

      {/* Probe Result & Defense Gap Report */}
      {report && (
        <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '14px' }}>
          {/* Evasion Banner */}
          <div style={{
            padding: '14px',
            borderRadius: '10px',
            background: report.evasion_successful ? 'rgba(244, 63, 94, 0.15)' : 'rgba(16, 185, 129, 0.15)',
            border: `1px solid ${report.evasion_successful ? '#f43f5e' : '#10b981'}`,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              {report.evasion_successful ? <ShieldAlert size={22} color="#f43f5e" /> : <CheckCircle2 size={22} color="#10b981" />}
              <div>
                <div style={{ fontSize: '14px', fontWeight: 800, color: report.evasion_successful ? '#fb7185' : '#34d399' }}>
                  {report.evasion_successful ? 'VULNERABILITY CONFIRMED: Defense Evaded' : 'PROBE INTERCEPTED: Defenses Held Firm'}
                </div>
                <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
                  Layer 1 Score: {report.layer1_score} • Decision: {report.layer1_decision} • Scam Shield: {report.scam_detected ? 'Intercepted' : 'Bypassed'}
                </div>
              </div>
            </div>

            <span className={`badge ${report.evasion_successful ? 'badge-hold' : 'badge-allow'}`}>
              {report.evasion_successful ? 'GAP DETECTED' : 'SECURE'}
            </span>
          </div>

          {/* Defense Gap Analysis */}
          <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
            <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#f8fafc', marginBottom: '8px' }}>
              Vulnerability Analysis
            </h4>
            <p style={{ fontSize: '12px', color: '#cbd5e1', lineHeight: 1.5 }}>
              {report.vulnerability_found}
            </p>

            <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#38bdf8', marginTop: '14px', marginBottom: '8px' }}>
              Recommended Remediation Policy
            </h4>
            <p style={{ fontSize: '12px', color: '#cbd5e1', lineHeight: 1.5 }}>
              {report.remediation_rule}
            </p>

            <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#34d399', marginTop: '14px', marginBottom: '8px' }}>
              Automated Defense Patch
            </h4>
            <pre style={{
              background: 'rgba(0,0,0,0.4)',
              padding: '10px',
              borderRadius: '6px',
              fontSize: '11px',
              fontFamily: 'monospace',
              color: '#a7f3d0',
              overflowX: 'auto'
            }}>
              {report.recommended_patch}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
