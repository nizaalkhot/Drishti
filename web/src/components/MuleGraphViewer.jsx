import React from 'react';
import { AlertOctagon, Database, ArrowRight, UserCheck, Smartphone, Landmark, Coins } from 'lucide-react';

export default function MuleGraphViewer({ analysis }) {
  const defaultAnalysis = {
    beneficiary_id: "MULE-AGGREGATOR-RING-1",
    mule_risk_score: 0.94,
    fan_in_count_24h: 6,
    rapid_passthrough_detected: true,
    shared_device_accounts: ["MULE-AGGREGATOR-RING-1-CASHOUT", "MULE-SECONDARY-PAYTM"],
    ring_cluster_id: "RING-CYBER-MULE-01",
    summary: "High fan-in velocity (6 unique senders in 24h); Rapid fund pass-through (>80% drained immediately); Device fingerprint shared with 2 other suspect accounts."
  };

  const data = analysis || defaultAnalysis;

  return (
    <div className="glass-panel" style={{ padding: '22px', display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '18px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '34px',
            height: '34px',
            borderRadius: '9px',
            background: 'rgba(168, 85, 247, 0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '1px solid rgba(168, 85, 247, 0.35)'
          }}>
            <AlertOctagon size={18} color="var(--accent-purple)" />
          </div>
          <div>
            <h2 style={{ fontSize: '16px', fontWeight: 800, color: '#f8fafc' }} className="font-display">
              BigQuery Mule-Ring Graph Intelligence
            </h2>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Topological 1-Hop & 2-Hop Graph Traversal (Shared Devices, Fan-In & Pass-Through)
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="badge" style={{ background: 'rgba(168, 85, 247, 0.12)', color: '#c084fc', border: '1px solid rgba(168, 85, 247, 0.3)' }}>
            <Database size={11} /> BIGQUERY LAKE
          </span>
          <span className="badge badge-hold font-mono tabular-nums">
            CLUSTER RISK: {data.mule_risk_score}
          </span>
        </div>
      </div>

      {/* Metrics Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '14px', marginBottom: '18px' }}>
        <div className="interactive-card" style={{ background: 'rgba(255,255,255,0.02)', padding: '14px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
          <div style={{ fontSize: '10px', color: 'var(--text-dim)', fontWeight: 700, letterSpacing: '0.04em' }} className="font-mono">
            24H FAN-IN VELOCITY
          </div>
          <div style={{ fontSize: '22px', fontWeight: 800, color: '#f8fafc', marginTop: '4px' }} className="font-mono tabular-nums">
            {data.fan_in_count_24h} Senders
          </div>
          <div style={{ fontSize: '11px', color: '#f59e0b', marginTop: '2px', fontWeight: 600 }}>⚠️ Anomalous spike (&gt;2)</div>
        </div>

        <div className="interactive-card" style={{ background: 'rgba(255,255,255,0.02)', padding: '14px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
          <div style={{ fontSize: '10px', color: 'var(--text-dim)', fontWeight: 700, letterSpacing: '0.04em' }} className="font-mono">
            RAPID PASS-THROUGH
          </div>
          <div style={{
            fontSize: '22px',
            fontWeight: 800,
            color: data.rapid_passthrough_detected ? '#ef4444' : '#10b981',
            marginTop: '4px'
          }} className="font-mono">
            {data.rapid_passthrough_detected ? 'ACTIVE (>80%)' : 'NORMAL'}
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text-dim)', marginTop: '2px' }}>Drained in &lt;15 mins</div>
        </div>

        <div className="interactive-card" style={{ background: 'rgba(255,255,255,0.02)', padding: '14px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
          <div style={{ fontSize: '10px', color: 'var(--text-dim)', fontWeight: 700, letterSpacing: '0.04em' }} className="font-mono">
            SHARED HARDWARE NODES
          </div>
          <div style={{ fontSize: '22px', fontWeight: 800, color: '#c084fc', marginTop: '4px' }} className="font-mono tabular-nums">
            {data.shared_device_accounts.length} Linked
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text-dim)', marginTop: '2px' }} className="font-mono">ID: DEV-SHARED-01</div>
        </div>
      </div>

      {/* Interactive Visual Graph Canvas */}
      <div style={{
        flex: 1,
        background: 'rgba(5, 8, 16, 0.85)',
        borderRadius: '14px',
        border: '1px solid var(--border-subtle)',
        position: 'relative',
        overflow: 'hidden',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px 24px',
        boxShadow: 'inset 0 2px 10px rgba(0, 0, 0, 0.5)'
      }}>
        {/* Background circuit grid */}
        <div style={{
          position: 'absolute',
          inset: 0,
          backgroundImage: 'radial-gradient(rgba(168, 85, 247, 0.08) 1px, transparent 1px)',
          backgroundSize: '24px 24px',
          pointerEvents: 'none'
        }} />

        {/* Graph Nodes Layout */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '92%', position: 'relative', zIndex: 1 }}>
          {/* Victims Fan-In */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, color: '#93c5fd', letterSpacing: '0.04em' }} className="font-mono">
              VICTIM REMITTERS
            </span>
            {['CUST-101 (Arun)', 'CUST-102 (Meera)', 'CUST-103 (Sunil)', 'CUST-104 (Pooja)'].map((victim, i) => (
              <div
                key={i}
                className="interactive-card"
                style={{
                  padding: '7px 12px',
                  borderRadius: '8px',
                  background: 'rgba(59, 130, 246, 0.12)',
                  border: '1px solid rgba(59, 130, 246, 0.3)',
                  fontSize: '11px',
                  fontWeight: 600,
                  color: '#93c5fd',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px'
                }}
              >
                <UserCheck size={13} color="#60a5fa" />
                <span className="font-mono">{victim}</span>
              </div>
            ))}
          </div>

          {/* Fan-in Arrows */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', color: 'rgba(255,255,255,0.25)' }}>
            <ArrowRight size={18} />
            <ArrowRight size={18} />
            <ArrowRight size={18} />
            <ArrowRight size={18} />
          </div>

          {/* Central Aggregator Mule Node */}
          <div className="interactive-card" style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            background: 'rgba(239, 68, 68, 0.14)',
            border: '2px solid #ef4444',
            borderRadius: '16px',
            padding: '18px',
            boxShadow: '0 0 32px rgba(239, 68, 68, 0.35)',
            textAlign: 'center',
            minWidth: '200px'
          }}>
            <div style={{
              width: '46px',
              height: '46px',
              borderRadius: '50%',
              background: '#ef4444',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '10px',
              boxShadow: '0 0 20px rgba(239, 68, 68, 0.7)'
            }}>
              <AlertOctagon size={24} color="#ffffff" />
            </div>
            <div style={{ fontSize: '13px', fontWeight: 800, color: '#ffffff' }} className="font-display">
              AGGREGATOR MULE
            </div>
            <div style={{ fontSize: '11px', color: '#fca5a5', fontWeight: 600, marginTop: '2px' }} className="font-mono">
              {data.beneficiary_id}
            </div>
            <span className="badge" style={{ background: 'rgba(239, 68, 68, 0.25)', color: '#fca5a5', marginTop: '8px', border: '1px solid rgba(239, 68, 68, 0.4)' }}>
              Cluster: {data.ring_cluster_id}
            </span>
          </div>

          {/* Pass-through Arrow */}
          <div style={{ color: '#ef4444' }}>
            <ArrowRight size={24} className="animate-pulse-slow" strokeWidth={2.5} />
          </div>

          {/* Cash-Out & Layering Mules */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, color: '#d8b4fe', letterSpacing: '0.04em' }} className="font-mono">
              CASHOUT / LAYERING
            </span>
            <div className="interactive-card" style={{
              padding: '10px 14px',
              borderRadius: '10px',
              background: 'rgba(168, 85, 247, 0.14)',
              border: '1px solid rgba(168, 85, 247, 0.4)',
              fontSize: '11px',
              color: '#d8b4fe',
              fontWeight: 600
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Landmark size={14} color="#c084fc" />
                <span>ATM Cash-Out Mule #1</span>
              </div>
              <div style={{ fontSize: '10px', color: 'var(--text-dim)', marginTop: '4px' }} className="font-mono">
                Device: DEV-MULE-01
              </div>
            </div>

            <div className="interactive-card" style={{
              padding: '10px 14px',
              borderRadius: '10px',
              background: 'rgba(168, 85, 247, 0.14)',
              border: '1px solid rgba(168, 85, 247, 0.4)',
              fontSize: '11px',
              color: '#d8b4fe',
              fontWeight: 600
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Coins size={14} color="#c084fc" />
                <span>Crypto Exchange Merchant</span>
              </div>
              <div style={{ fontSize: '10px', color: '#f87171', marginTop: '4px' }}>
                Drained in 8 mins
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Summary Banner */}
      <div style={{
        marginTop: '16px',
        background: 'rgba(168, 85, 247, 0.08)',
        padding: '14px 18px',
        borderRadius: '10px',
        borderLeft: '4px solid var(--accent-purple)',
        border: '1px solid rgba(168, 85, 247, 0.2)'
      }}>
        <div style={{ fontSize: '11px', fontWeight: 800, color: '#c084fc', textTransform: 'uppercase', letterSpacing: '0.04em' }} className="font-mono">
          MULE GRAPH REASONING TRACE
        </div>
        <div style={{ fontSize: '12px', color: 'var(--text-main)', marginTop: '4px', lineHeight: 1.5 }}>
          {data.summary}
        </div>
      </div>
    </div>
  );
}
