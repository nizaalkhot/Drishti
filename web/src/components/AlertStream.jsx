import React from 'react';
import { Activity, Clock, Cpu, ShieldAlert } from 'lucide-react';

export default function AlertStream({ transactions, selectedTx, onSelectTx }) {
  return (
    <div className="glass-panel" style={{ padding: '18px 20px', display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '6px',
            background: 'rgba(6, 182, 212, 0.12)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '1px solid rgba(6, 182, 212, 0.28)'
          }}>
            <Activity size={16} color="var(--accent-cyan)" />
          </div>
          <div>
            <h2 style={{ fontSize: '15px', fontWeight: 800, color: 'var(--text-main)', letterSpacing: '-0.02em' }} className="font-display">
              Real-Time Ingestion Stream
            </h2>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Sub-millisecond UPI scam detection and telemetry mesh
            </p>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="badge" style={{ background: 'rgba(6, 182, 212, 0.08)', color: '#38bdf8', border: '1px solid rgba(6, 182, 212, 0.25)' }}>
            <Cpu size={12} /> L1 SLA: &lt;15ms
          </span>
          <span style={{ fontSize: '11px', color: 'var(--text-dim)', fontWeight: 700 }} className="font-mono">
            {transactions.length} EVENTS
          </span>
        </div>
      </div>

      {/* Institutional Telemetry Strip */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        gap: '8px',
        padding: '10px 12px',
        background: 'rgba(0, 0, 0, 0.35)',
        borderRadius: '8px',
        border: '1px solid var(--border-subtle)',
        marginBottom: '14px'
      }}>
        <div>
          <div style={{ fontSize: '9px', color: 'var(--text-dim)', fontWeight: 700, letterSpacing: '0.05em' }} className="font-mono">
            GATE LATENCY
          </div>
          <div style={{ fontSize: '13px', fontWeight: 700, color: '#38bdf8', marginTop: '2px' }} className="font-mono tabular-nums">
            0.04 ms
          </div>
        </div>
        <div>
          <div style={{ fontSize: '9px', color: 'var(--text-dim)', fontWeight: 700, letterSpacing: '0.05em' }} className="font-mono">
            GOLDEN RECALL
          </div>
          <div style={{ fontSize: '13px', fontWeight: 700, color: 'var(--risk-allow)', marginTop: '2px' }} className="font-mono tabular-nums">
            100.0%
          </div>
        </div>
        <div>
          <div style={{ fontSize: '9px', color: 'var(--text-dim)', fontWeight: 700, letterSpacing: '0.05em' }} className="font-mono">
            I4C REGISTRY
          </div>
          <div style={{ fontSize: '13px', fontWeight: 700, color: '#e2e8f0', marginTop: '2px' }} className="font-mono">
            SYNCHRONIZED
          </div>
        </div>
        <div>
          <div style={{ fontSize: '9px', color: 'var(--text-dim)', fontWeight: 700, letterSpacing: '0.05em' }} className="font-mono">
            ENGINE STATUS
          </div>
          <div style={{ fontSize: '13px', fontWeight: 700, color: 'var(--risk-allow)', marginTop: '2px' }} className="font-mono">
            AUTONOMOUS
          </div>
        </div>
      </div>

      {/* Stream List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', overflowY: 'auto', flex: 1, paddingRight: '4px' }}>
        {transactions.length === 0 ? (
          <div style={{
            textAlign: 'center',
            padding: '50px 20px',
            color: 'var(--text-dim)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '12px',
            background: 'radial-gradient(circle at center, rgba(6, 182, 212, 0.04) 0%, rgba(0, 0, 0, 0.2) 70%)',
            borderRadius: '10px',
            border: '1px dashed rgba(255, 255, 255, 0.08)'
          }}>
            <div style={{
              width: '44px',
              height: '44px',
              borderRadius: '50%',
              background: 'rgba(6, 182, 212, 0.08)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              border: '1px solid rgba(6, 182, 212, 0.25)',
              position: 'relative'
            }}>
              <ShieldAlert size={22} color="var(--accent-cyan)" />
            </div>
            <div>
              <p style={{ fontWeight: 700, color: 'var(--text-main)', fontSize: '13px', letterSpacing: '0.02em' }} className="font-mono">
                [SENSOR ARRAY ACTIVE // LISTENING ON UPI STREAM]
              </p>
              <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
                Inject an attack scenario from the top toolbar or submit a payment via the phone simulator
              </p>
            </div>
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
                className="interactive-card"
                style={{
                  padding: '12px 14px',
                  borderRadius: '8px',
                  background: isSelected ? 'rgba(6, 182, 212, 0.12)' : 'rgba(255, 255, 255, 0.02)',
                  border: isSelected ? '1px solid rgba(6, 182, 212, 0.5)' : '1px solid var(--border-subtle)',
                  cursor: 'pointer',
                  boxShadow: isSelected ? '0 0 16px rgba(6, 182, 212, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.08)' : '0 2px 6px rgba(0, 0, 0, 0.3)'
                }}
              >
                {/* Upper line: ID, decision badge, latency */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexWrap: 'wrap' }}>
                    <span style={{ fontSize: '12px', fontWeight: 800, color: 'var(--text-main)', letterSpacing: '0.04em' }} className="font-mono">
                      {tx.transaction_id}
                    </span>
                    {isAllow && <span className="badge badge-allow">ALLOW</span>}
                    {isIntervene && <span className="badge badge-intervene">INTERVENTION</span>}
                    {isHold && <span className="badge badge-hold">HOLD</span>}
                    {tx.consortium_reference && (
                      <span className="badge badge-hold">
                        I4C MATCH
                      </span>
                    )}
                    {tx.semantic_cache_hit && (
                      <span className="badge badge-allow">
                        CACHE HIT
                      </span>
                    )}
                    {tx.friction_tier === 'TIER_1_CHIP' && (
                      <span className="badge badge-intervene">
                        TIER 1 CHIP
                      </span>
                    )}
                    {tx.friction_tier === 'HARD_BLOCK' && (
                      <span className="badge badge-hold">
                        HARD BLOCK
                      </span>
                    )}
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', color: 'var(--text-dim)' }} className="font-mono tabular-nums">
                    <Clock size={11} />
                    <span>L1: {tx.layer1_latency_ms}ms • Tot: {tx.total_latency_ms}ms</span>
                  </div>
                </div>

                {/* Middle line: Amount and Payee */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '2px' }}>
                  <div>
                    <span style={{ fontSize: '11px', color: 'var(--text-dim)' }}>To: </span>
                    <span style={{ fontSize: '12px', fontWeight: 600, color: '#e2e8f0' }} className="font-mono">{tx.receiver_vpa}</span>
                  </div>
                  <div style={{
                    fontSize: '15px',
                    fontWeight: 800,
                    color: isAllow ? 'var(--risk-allow)' : isIntervene ? 'var(--risk-intervene)' : 'var(--risk-hold)'
                  }} className="font-mono tabular-nums">
                    ₹{tx.amount.toLocaleString('en-IN')}
                  </div>
                </div>

                {/* Remark & Typology */}
                {tx.remark && (
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '5px', fontStyle: 'italic', background: 'rgba(0, 0, 0, 0.25)', padding: '4px 8px', borderRadius: '4px' }}>
                    "{tx.remark}"
                  </div>
                )}

                {/* Risk score bar */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '8px' }}>
                  <div style={{ flex: 1, height: '4px', background: 'rgba(255,255,255,0.06)', borderRadius: '2px', overflow: 'hidden' }}>
                    <div style={{
                      width: `${Math.min(100, tx.risk_score * 100)}%`,
                      height: '100%',
                      background: isAllow
                        ? 'linear-gradient(90deg, #10b981 0%, #34d399 100%)'
                        : isIntervene
                        ? 'linear-gradient(90deg, #d97706 0%, #f59e0b 100%)'
                        : 'linear-gradient(90deg, #dc2626 0%, #ef4444 100%)',
                      borderRadius: '2px'
                    }} />
                  </div>
                  <span style={{
                    fontSize: '11px',
                    fontWeight: 800,
                    color: isAllow ? 'var(--risk-allow)' : isIntervene ? 'var(--risk-intervene)' : 'var(--risk-hold)'
                  }} className="font-mono tabular-nums">
                    Score: {tx.risk_score}
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
