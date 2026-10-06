import React from 'react';
import { Activity, Clock, Cpu, ShieldAlert, ArrowRight, Zap } from 'lucide-react';

export default function AlertStream({ transactions, selectedTx, onSelectTx, onInjectScenario }) {
  return (
    <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '8px',
            background: 'rgba(99, 102, 241, 0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '1px solid rgba(99, 102, 241, 0.3)'
          }}>
            <Activity size={17} color="var(--accent-primary)" />
          </div>
          <div>
            <h2 style={{ fontSize: '15px', fontWeight: 800, color: 'var(--text-main)' }} className="font-display">
              Real-Time Ingestion Stream
            </h2>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Sub-millisecond UPI fraud detection pipeline
            </p>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="badge" style={{ background: 'rgba(99, 102, 241, 0.12)', color: '#a5b4fc', border: '1px solid rgba(99, 102, 241, 0.25)' }}>
            <Cpu size={12} /> LAYER 1: &lt;15ms SLA
          </span>
          <span style={{ fontSize: '11px', color: 'var(--text-dim)', fontWeight: 700 }} className="font-mono">
            {transactions.length} EVENTS
          </span>
        </div>
      </div>

      {/* Stream List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', overflowY: 'auto', flex: 1, paddingRight: '4px' }}>
        {transactions.length === 0 ? (
          <div style={{
            textAlign: 'center',
            padding: '60px 20px',
            color: 'var(--text-dim)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '12px',
            background: 'rgba(255, 255, 255, 0.01)',
            borderRadius: '12px',
            border: '1px dashed var(--border-subtle)'
          }}>
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '50%',
              background: 'rgba(99, 102, 241, 0.08)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              border: '1px solid rgba(99, 102, 241, 0.2)'
            }}>
              <ShieldAlert size={24} color="var(--accent-primary)" />
            </div>
            <div>
              <p style={{ fontWeight: 700, color: 'var(--text-main)', fontSize: '14px' }}>Waiting for incoming UPI transactions...</p>
              <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
                Use the customer phone simulator or trigger an attack scenario above
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
                  padding: '14px',
                  borderRadius: '12px',
                  background: isSelected ? 'rgba(99, 102, 241, 0.16)' : 'rgba(255, 255, 255, 0.02)',
                  border: isSelected ? '1px solid rgba(99, 102, 241, 0.55)' : '1px solid var(--border-subtle)',
                  cursor: 'pointer',
                  boxShadow: isSelected ? '0 0 20px rgba(99, 102, 241, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.1)' : '0 2px 6px rgba(0, 0, 0, 0.3)'
                }}
              >
                {/* Upper line: ID, decision badge, latency */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', flexWrap: 'wrap' }}>
                    <span style={{ fontSize: '12px', fontWeight: 800, color: 'var(--text-main)', letterSpacing: '0.04em' }} className="font-mono">
                      {tx.transaction_id}
                    </span>
                    {isAllow && <span className="badge badge-allow">ALLOW</span>}
                    {isIntervene && <span className="badge badge-intervene">SCAM INTERVENTION</span>}
                    {isHold && <span className="badge badge-hold">HOLD</span>}
                    {tx.consortium_reference && (
                      <span className="badge" style={{ background: 'rgba(239, 68, 68, 0.15)', color: '#f87171', border: '1px solid rgba(239, 68, 68, 0.3)' }}>
                        I4C MATCH
                      </span>
                    )}
                    {tx.semantic_cache_hit && (
                      <span className="badge" style={{ background: 'rgba(16, 185, 129, 0.15)', color: '#34d399', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
                        CACHE HIT
                      </span>
                    )}
                    {tx.friction_tier === 'TIER_1_CHIP' && (
                      <span className="badge" style={{ background: 'rgba(245, 158, 11, 0.15)', color: '#fbbf24', border: '1px solid rgba(245, 158, 11, 0.3)' }}>
                        TIER 1 CHIP
                      </span>
                    )}
                    {tx.friction_tier === 'HARD_BLOCK' && (
                      <span className="badge" style={{ background: 'rgba(239, 68, 68, 0.15)', color: '#ef4444', border: '1px solid rgba(239, 68, 68, 0.3)' }}>
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
                    fontSize: '16px',
                    fontWeight: 800,
                    color: isAllow ? '#34d399' : isIntervene ? '#fbbf24' : '#f87171'
                  }} className="font-mono tabular-nums">
                    ₹{tx.amount.toLocaleString('en-IN')}
                  </div>
                </div>

                {/* Remark & Typology */}
                {tx.remark && (
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px', fontStyle: 'italic', background: 'rgba(0, 0, 0, 0.2)', padding: '4px 8px', borderRadius: '4px' }}>
                    "{tx.remark}"
                  </div>
                )}

                {/* Risk score bar */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginTop: '10px' }}>
                  <div style={{ flex: 1, height: '5px', background: 'rgba(255,255,255,0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                    <div style={{
                      width: `${Math.min(100, tx.risk_score * 100)}%`,
                      height: '100%',
                      background: isAllow
                        ? 'linear-gradient(90deg, #10b981 0%, #34d399 100%)'
                        : isIntervene
                        ? 'linear-gradient(90deg, #f59e0b 0%, #fbbf24 100%)'
                        : 'linear-gradient(90deg, #dc2626 0%, #ef4444 100%)',
                      borderRadius: '3px',
                      boxShadow: isAllow
                        ? '0 0 8px rgba(16, 185, 129, 0.5)'
                        : isIntervene
                        ? '0 0 8px rgba(245, 158, 11, 0.5)'
                        : '0 0 8px rgba(239, 68, 68, 0.5)'
                    }} />
                  </div>
                  <span style={{
                    fontSize: '11px',
                    fontWeight: 800,
                    color: isAllow ? '#34d399' : isIntervene ? '#fbbf24' : '#f87171'
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
