import React from 'react';
import { Activity, Clock, ShieldCheck, AlertTriangle, ShieldAlert, ArrowUpRight, Cpu } from 'lucide-react';

export default function AlertStream({ transactions, selectedTx, onSelectTx }) {
  return (
    <div className="glass-panel" style={{ padding: '16px', display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Activity size={18} color="var(--accent-indigo)" />
          <h2 style={{ fontSize: '15px', fontWeight: 700 }}>Real-Time Ingestion Stream</h2>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span className="badge" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#818cf8' }}>
            <Cpu size={11} /> LAYER 1: &lt;15ms SLA
          </span>
          <span style={{ fontSize: '11px', color: 'var(--text-dim)', fontWeight: 600 }}>
            {transactions.length} EVENTS
          </span>
        </div>
      </div>

      {/* Stream List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', overflowY: 'auto', flex: 1, paddingRight: '4px' }}>
        {transactions.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px 10px', color: 'var(--text-dim)' }}>
            <p>Waiting for incoming UPI transactions...</p>
            <p style={{ fontSize: '11px', marginTop: '6px' }}>Use the scenario injector or customer phone simulator</p>
          </div>
        ) : (
          transactions.map((tx) => {
            const isSelected = selectedTx && selectedTx.transaction_id === tx.transaction_id;
            const isIntervene = tx.decision === 'INTERVENE';
            const isHold = tx.decision === 'HOLD';
            const isAllow = tx.decision === 'ALLOW';

            return (
              <div
                key={tx.transaction_id}
                onClick={() => onSelectTx(tx)}
                style={{
                  padding: '12px',
                  borderRadius: '10px',
                  background: isSelected ? 'rgba(99, 102, 241, 0.18)' : 'rgba(255, 255, 255, 0.02)',
                  border: isSelected ? '1px solid rgba(99, 102, 241, 0.5)' : '1px solid var(--border-subtle)',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                  boxShadow: isSelected ? '0 0 16px rgba(99, 102, 241, 0.2)' : 'none'
                }}
              >
                {/* Upper line: ID, decision badge, latency */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span style={{ fontSize: '12px', fontWeight: 800, color: 'var(--text-main)', letterSpacing: '0.02em' }}>
                      {tx.transaction_id}
                    </span>
                    {isAllow && <span className="badge badge-allow">ALLOW</span>}
                    {isIntervene && <span className="badge badge-intervene">SCAM INTERVENTION</span>}
                    {isHold && <span className="badge badge-hold">HOLD</span>}
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '10px', color: 'var(--text-dim)' }}>
                    <Clock size={11} />
                    <span>L1: {tx.layer1_latency_ms}ms • Total: {tx.total_latency_ms}ms</span>
                  </div>
                </div>

                {/* Middle line: Amount and Payee */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div>
                    <span style={{ fontSize: '11px', color: 'var(--text-dim)' }}>To: </span>
                    <span style={{ fontSize: '12px', fontWeight: 600, color: '#e2e8f0' }}>{tx.receiver_vpa}</span>
                  </div>
                  <div style={{ fontSize: '15px', fontWeight: 800, color: isAllow ? '#34d399' : isIntervene ? '#fbbf24' : '#fb7185' }}>
                    ₹{tx.amount.toLocaleString('en-IN')}
                  </div>
                </div>

                {/* Remark & Typology */}
                {tx.remark && (
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px', fontStyle: 'italic' }}>
                    "{tx.remark}"
                  </div>
                )}

                {/* Risk score bar */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '8px' }}>
                  <div style={{ flex: 1, height: '4px', background: 'rgba(255,255,255,0.08)', borderRadius: '2px', overflow: 'hidden' }}>
                    <div style={{
                      width: `${tx.risk_score * 100}%`,
                      height: '100%',
                      background: isAllow ? '#10b981' : isIntervene ? '#f59e0b' : '#f43f5e',
                      borderRadius: '2px'
                    }} />
                  </div>
                  <span style={{ fontSize: '10px', fontWeight: 700, color: isAllow ? '#34d399' : isIntervene ? '#fbbf24' : '#fb7185' }}>
                    Risk: {tx.risk_score}
                  </span>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
