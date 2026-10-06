import React, { useState } from 'react';
import { FileText, Eye } from 'lucide-react';

export default function CaseListView({ cases, onSelectCase }) {
  const [filter, setFilter] = useState('ALL');

  const filteredCases = cases.filter(c => {
    if (filter === 'ALL') return true;
    return c.status === filter;
  });

  return (
    <div className="glass-panel" style={{ padding: '22px', display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '18px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '10px',
            background: 'rgba(99, 102, 241, 0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '1px solid rgba(99, 102, 241, 0.35)'
          }}>
            <FileText size={18} color="var(--accent-primary)" />
          </div>
          <div>
            <h2 style={{ fontSize: '16px', fontWeight: 800, color: '#f8fafc' }} className="font-display">
              Investigator Copilot Case Queue
            </h2>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Autonomous Evidence Synthesis • Human-in-the-Loop FIU-IND STR Filing
            </p>
          </div>
        </div>

        {/* Filters */}
        <div style={{
          display: 'flex',
          gap: '4px',
          background: 'rgba(15, 23, 42, 0.6)',
          padding: '4px',
          borderRadius: '10px',
          border: '1px solid var(--border-subtle)'
        }}>
          {['ALL', 'PENDING_REVIEW', 'ACCOUNT_FROZEN', 'STR_FILED'].map((f) => {
            const isSelected = filter === f;
            return (
              <button
                key={f}
                onClick={() => setFilter(f)}
                style={{
                  border: 'none',
                  background: isSelected ? 'linear-gradient(135deg, #4f46e5 0%, #6366f1 100%)' : 'transparent',
                  color: isSelected ? '#fff' : 'var(--text-muted)',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '10px',
                  fontWeight: 700,
                  padding: '5px 10px',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                  boxShadow: isSelected ? '0 2px 8px rgba(99, 102, 241, 0.4)' : 'none'
                }}
              >
                {f.replace('_', ' ')}
              </button>
            );
          })}
        </div>
      </div>

      {/* Case Table / Cards */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', overflowY: 'auto', flex: 1 }}>
        {filteredCases.length === 0 ? (
          <div style={{
            textAlign: 'center',
            padding: '50px 20px',
            color: 'var(--text-dim)',
            background: 'rgba(255, 255, 255, 0.01)',
            borderRadius: '12px',
            border: '1px dashed var(--border-subtle)'
          }}>
            No cases matching filter "{filter}"
          </div>
        ) : (
          filteredCases.map((c) => {
            const tx = c.transaction;
            return (
              <div
                key={c.case_id}
                onClick={() => onSelectCase(c)}
                className="interactive-card"
                style={{
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '12px',
                  padding: '16px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  cursor: 'pointer'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                  <div style={{
                    width: '40px',
                    height: '40px',
                    borderRadius: '10px',
                    background: 'rgba(99, 102, 241, 0.12)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: '#818cf8',
                    fontWeight: 800,
                    fontSize: '12px',
                    border: '1px solid rgba(99, 102, 241, 0.25)'
                  }} className="font-mono">
                    STR
                  </div>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontSize: '14px', fontWeight: 800, color: '#f8fafc' }} className="font-mono">
                        {c.case_id}
                      </span>
                      <span className={`badge ${c.status === 'ACCOUNT_FROZEN' ? 'badge-hold' : c.status === 'STR_FILED' ? 'badge-allow' : 'badge-intervene'}`}>
                        {c.status}
                      </span>
                    </div>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
                      <span className="font-mono">{tx.sender_vpa}</span> ➔ <span className="font-mono">{tx.receiver_vpa}</span>
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '16px', fontWeight: 800, color: '#f43f5e' }} className="font-mono tabular-nums">
                      ₹{tx.amount.toLocaleString('en-IN')}
                    </div>
                    <div style={{ fontSize: '10px', color: 'var(--text-dim)', marginTop: '2px' }}>
                      Typology: {c.scam_decision.scam_typology}
                    </div>
                  </div>

                  <button
                    className="btn btn-outline"
                    style={{ padding: '7px 14px', fontSize: '11px', display: 'flex', alignItems: 'center', gap: '6px' }}
                  >
                    <Eye size={13} /> Inspect Dossier
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
