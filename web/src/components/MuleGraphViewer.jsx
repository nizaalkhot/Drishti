import React, { useState } from 'react';
import { AlertOctagon, Database, ArrowRight, UserCheck, Landmark, Coins, GitFork } from 'lucide-react';

function RemitterColumn({ remitters, label, subtitle, compact }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: compact ? '6px' : '10px', minWidth: compact ? '130px' : '150px' }}>
      <span style={{ fontSize: compact ? '10px' : '11px', fontWeight: 700, color: '#93c5fd', letterSpacing: '0.04em' }} className="font-mono">
        {label}
      </span>
      {remitters.map((victim, i) => (
        <div
          key={i}
          className="interactive-card"
          style={{
            padding: compact ? '5px 8px' : '7px 12px',
            borderRadius: compact ? '6px' : '8px',
            background: 'rgba(59, 130, 246, 0.12)',
            border: '1px solid rgba(59, 130, 246, 0.3)',
            fontSize: compact ? '10px' : '11px',
            fontWeight: 600,
            color: '#93c5fd',
            display: 'flex',
            alignItems: 'center',
            gap: compact ? '6px' : '8px'
          }}
        >
          <UserCheck size={compact ? 11 : 13} color="#60a5fa" />
          <span className="font-mono">{victim}</span>
        </div>
      ))}
      {subtitle && (
        <span style={{ fontSize: '9px', color: '#60a5fa' }} className="font-mono">{subtitle}</span>
      )}
    </div>
  );
}

function AggregatorMuleCard({ beneficiaryId, clusterId, transitTime, compact }) {
  return (
    <div className="interactive-card" style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      background: 'rgba(239, 68, 68, 0.14)',
      border: '2px solid #ef4444',
      borderRadius: compact ? '12px' : '16px',
      padding: compact ? '12px' : '18px',
      boxShadow: compact ? '0 0 20px rgba(239, 68, 68, 0.35)' : '0 0 32px rgba(239, 68, 68, 0.35)',
      textAlign: 'center',
      minWidth: compact ? '150px' : '200px'
    }}>
      <div style={{
        width: compact ? '32px' : '46px',
        height: compact ? '32px' : '46px',
        borderRadius: '50%',
        background: '#ef4444',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: compact ? '6px' : '10px',
        boxShadow: compact ? '0 0 15px rgba(239, 68, 68, 0.7)' : '0 0 20px rgba(239, 68, 68, 0.7)'
      }}>
        <AlertOctagon size={compact ? 16 : 24} color="#ffffff" />
      </div>
      <div style={{ fontSize: compact ? '11px' : '13px', fontWeight: 800, color: '#ffffff' }} className="font-display">
        {compact ? 'HOP 1: ESCROW MULE' : 'AGGREGATOR MULE'}
      </div>
      <div style={{ fontSize: compact ? '10px' : '11px', color: '#fca5a5', fontWeight: 600, marginTop: '2px' }} className="font-mono">
        {beneficiaryId}
      </div>
      <span className="badge" style={{ background: 'rgba(239, 68, 68, 0.25)', color: '#fca5a5', marginTop: compact ? '6px' : '8px', fontSize: compact ? '9px' : '10px', border: '1px solid rgba(239, 68, 68, 0.4)' }}>
        {transitTime || `Cluster: ${clusterId}`}
      </span>
    </div>
  );
}

function SmurfLayerColumn({ smurfs }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', minWidth: '140px' }}>
      <span style={{ fontSize: '10px', fontWeight: 700, color: '#facc15', letterSpacing: '0.04em' }} className="font-mono">
        HOP 2: SMURF SPLIT (&lt;₹50k)
      </span>
      {smurfs.map((smurf, i) => (
        <div
          key={i}
          className="interactive-card"
          style={{
            padding: '5px 8px',
            borderRadius: '6px',
            background: 'rgba(234, 179, 8, 0.12)',
            border: '1px solid rgba(234, 179, 8, 0.35)',
            fontSize: '10px',
            fontWeight: 600,
            color: '#fef08a'
          }}
        >
          <span className="font-mono">{smurf}</span>
        </div>
      ))}
      <span style={{ fontSize: '9px', color: '#eab308' }} className="font-mono">Structured evasion</span>
    </div>
  );
}

function ExtractionSinkList({ label, compact }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: compact ? '6px' : '14px', minWidth: compact ? '140px' : 'auto' }}>
      <span style={{ fontSize: compact ? '10px' : '11px', fontWeight: 700, color: '#d8b4fe', letterSpacing: '0.04em' }} className="font-mono">
        {label}
      </span>
      <div className="interactive-card" style={{
        padding: compact ? '6px 8px' : '10px 14px',
        borderRadius: compact ? '6px' : '10px',
        background: 'rgba(168, 85, 247, 0.14)',
        border: '1px solid rgba(168, 85, 247, 0.4)',
        fontSize: compact ? '10px' : '11px',
        color: '#d8b4fe',
        fontWeight: 600
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <Landmark size={compact ? 12 : 14} color="#c084fc" />
          <span>Cardless ATM Sinks</span>
        </div>
        <div style={{ fontSize: compact ? '9px' : '10px', color: 'var(--text-dim)', marginTop: compact ? '2px' : '4px' }} className="font-mono">
          Mumbai Bandra #44
        </div>
      </div>

      <div className="interactive-card" style={{
        padding: compact ? '6px 8px' : '10px 14px',
        borderRadius: compact ? '6px' : '10px',
        background: 'rgba(168, 85, 247, 0.14)',
        border: '1px solid rgba(168, 85, 247, 0.4)',
        fontSize: compact ? '10px' : '11px',
        color: '#d8b4fe',
        fontWeight: 600
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
          <Coins size={compact ? 12 : 14} color="#c084fc" />
          <span>Crypto OTC Desk</span>
        </div>
        <div style={{ fontSize: compact ? '9px' : '10px', color: '#f87171', marginTop: compact ? '2px' : '4px' }}>
          USDT P2P Escrow
        </div>
      </div>
    </div>
  );
}

export default function MuleGraphViewer({ analysis }) {
  const [isMultiHopMode, setIsMultiHopMode] = useState(true);

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
    <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '32px',
            height: '32px',
            borderRadius: '6px',
            background: 'rgba(6, 182, 212, 0.12)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '1px solid rgba(6, 182, 212, 0.3)'
          }}>
            <AlertOctagon size={17} color="var(--accent-cyan)" />
          </div>
          <div>
            <h2 style={{ fontSize: '15px', fontWeight: 800, color: '#f8fafc', letterSpacing: '-0.02em' }} className="font-display">
              BigQuery Mule-Ring Graph Intelligence
            </h2>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Topological 4-Hop Smurfing Traversal (Shared Devices, Fan-In & Pass-Through)
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <button
            type="button"
            onClick={() => setIsMultiHopMode(!isMultiHopMode)}
            style={{
              background: isMultiHopMode ? 'rgba(168, 85, 247, 0.2)' : 'rgba(255, 255, 255, 0.05)',
              border: isMultiHopMode ? '1px solid #c084fc' : '1px solid rgba(255, 255, 255, 0.1)',
              color: isMultiHopMode ? '#e9d5ff' : '#94a3b8',
              borderRadius: '6px',
              padding: '4px 8px',
              fontSize: '11px',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '5px'
            }}
          >
            <GitFork size={13} />
            {isMultiHopMode ? 'Multi-Hop Smurfing (4 Hops Active)' : 'Switch to 4-Hop Mode'}
          </button>
          <span className="badge" style={{ background: 'rgba(6, 182, 212, 0.08)', color: '#38bdf8', border: '1px solid rgba(6, 182, 212, 0.25)' }}>
            <Database size={11} /> BIGQUERY LAKE
          </span>
          <span className="badge badge-hold font-mono tabular-nums">
            CLUSTER RISK: {data.mule_risk_score}
          </span>
        </div>
      </div>

      {/* Metrics Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginBottom: '16px' }}>
        <div className="interactive-card" style={{ background: 'rgba(255,255,255,0.02)', padding: '12px 14px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
          <div style={{ fontSize: '9px', color: 'var(--text-dim)', fontWeight: 700, letterSpacing: '0.05em' }} className="font-mono">
            24H FAN-IN VELOCITY
          </div>
          <div style={{ fontSize: '20px', fontWeight: 800, color: '#f8fafc', marginTop: '4px' }} className="font-mono tabular-nums">
            {data.fan_in_count_24h} Senders
          </div>
          <div style={{ fontSize: '10px', color: 'var(--risk-intervene)', marginTop: '2px', fontWeight: 700 }} className="font-mono">[ANOMALOUS SPIKE &gt; 2]</div>
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

        {/* Unified Graph Nodes Layout */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          width: isMultiHopMode ? '96%' : '90%',
          position: 'relative',
          zIndex: 1,
          gap: '8px'
        }}>
          <RemitterColumn
            remitters={isMultiHopMode ? ['CUST-101 (Arun)', 'CUST-102 (Meera)', 'CUST-103 (Sunil)'] : ['CUST-101 (Arun)', 'CUST-102 (Meera)', 'CUST-103 (Sunil)', 'CUST-104 (Pooja)']}
            label={isMultiHopMode ? "HOP 0: REMITTERS" : "VICTIM REMITTERS"}
            subtitle={isMultiHopMode ? "Inflow: ₹4,80,000" : null}
            compact={isMultiHopMode}
          />

          <ArrowRight size={18} color="rgba(255,255,255,0.4)" />

          <AggregatorMuleCard
            beneficiaryId={data.beneficiary_id}
            clusterId={data.ring_cluster_id}
            transitTime={isMultiHopMode ? "Transit: 42s" : null}
            compact={isMultiHopMode}
          />

          <ArrowRight size={18} color="#ef4444" className="animate-pulse-slow" />

          {isMultiHopMode && (
            <>
              <SmurfLayerColumn
                smurfs={['MULE-SMURF-A (₹49,500)', 'MULE-SMURF-B (₹48,800)', 'MULE-SMURF-C (₹49,200)']}
              />
              <ArrowRight size={18} color="#c084fc" className="animate-pulse-slow" />
            </>
          )}

          <ExtractionSinkList
            label={isMultiHopMode ? "HOP 3: EXTRACTION SINKS" : "CASHOUT / LAYERING"}
            compact={isMultiHopMode}
          />
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
