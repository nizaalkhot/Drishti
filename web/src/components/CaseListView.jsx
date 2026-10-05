import React, { useState } from 'react';
import { FileText, Lock, CheckCircle2, AlertTriangle, Clock, Eye } from 'lucide-react';

export default function CaseListView({ cases, onSelectCase }) {
  const [filter, setFilter] = useState('ALL');

  const filteredCases = cases.filter(c => {
    if (filter === 'ALL') return true;
    return c.status === filter;
  });

  return (
    <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <FileText size={20} color="var(--accent-indigo)" />
          <div>
            <h2 style={{ fontSize: '16px', fontWeight: 800 }}>Investigator Copilot Case Queue</h2>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Autonomous Evidence Synthesis • Human-in-the-Loop FIU-IND STR Filing
            </p>
          </div>
        </div>

        {/* Filters */}
        <div style={{ display: 'flex', gap: '4px', background: 'rgba(255,255,255,0.03)', padding: '3px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
          {['ALL', 'PENDING_REVIEW', 'ACCOUNT_FROZEN', 'STR_FILED'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              style={{
                border: 'none',
                background: filter === f ? 'var(--accent-indigo)' : 'transparent',
                color: filter === f ? '#fff' : 'var(--text-muted)',
                fontSize: '10px',
                fontWeight: 700,
                padding: '4px 8px',
                borderRadius: '6px',
                cursor: 'pointer'
              }}
            >
              {f.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Case Table / Cards */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', overflowY: 'auto', flex: 1 }}>
        {filteredCases.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-dim)' }}>
            No cases matching filter "{filter}"
          </div>
        ) : (
          filteredCases.map((c) => {
            const tx = c.transaction;
            const str = c.str_report;
            return (
              <div
                key={c.case_id}
                onClick={() => onSelectCase(c)}
                style={{
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: '10px',
                  padding: '14px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{
                    width: '36px',
                    height: '36px',
                    borderRadius: '8px',
                    background: 'rgba(99, 102, 241, 0.15)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--accent-indigo)',
                    fontWeight: 800,
                    fontSize: '12px'
                  }}>
                    STR
                  </div>
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontSize: '14px', fontWeight: 800, color: '#f8fafc' }}>{c.case_id}</span>
                      <span className={`badge ${c.status === 'ACCOUNT_FROZEN' ? 'badge-hold' : c.status === 'STR_FILED' ? 'badge-allow' : 'badge-intervene'}`}>
                        {c.status}
                      </span>
                    </div>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>
                      Victim: {tx.sender_vpa} ➔ Beneficiary: {tx.receiver_vpa}
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '15px', fontWeight: 800, color: '#f43f5e' }}>
                      ₹{tx.amount.toLocaleString('en-IN')}
                    </div>
                    <div style={{ fontSize: '10px', color: 'var(--text-dim)' }}>
                      Typology: {c.scam_decision.scam_typology}
                    </div>
                  </div>

                  <button
                    className="btn btn-outline"
                    style={{ padding: '6px 12px', fontSize: '11px' }}
                  >
                    <Eye size={12} /> Inspect Dossier
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
