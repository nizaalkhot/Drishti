import React from 'react';
import { AlertOctagon, Share2, Database, ShieldAlert, Cpu, ArrowRight } from 'lucide-react';

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
    <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <AlertOctagon size={20} color="var(--accent-purple)" />
          <div>
            <h2 style={{ fontSize: '16px', fontWeight: 800 }}>BigQuery Mule-Ring Graph Intelligence</h2>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Topological 1-Hop & 2-Hop Graph Traversal (Shared Devices, Fan-In & Pass-Through)
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="badge" style={{ background: 'rgba(168, 85, 247, 0.15)', color: '#c084fc', border: '1px solid rgba(168, 85, 247, 0.3)' }}>
            <Database size={11} /> BIGQUERY LAKE
          </span>
          <span className="badge badge-hold">
            CLUSTER RISK: {data.mule_risk_score}
          </span>
        </div>
      </div>

      {/* Metrics Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginBottom: '16px' }}>
        <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
          <div style={{ fontSize: '10px', color: 'var(--text-dim)', fontWeight: 700 }}>24H FAN-IN VELOCITY</div>
          <div style={{ fontSize: '20px', fontWeight: 800, color: '#f8fafc', marginTop: '2px' }}>
            {data.fan_in_count_24h} Senders
          </div>
          <div style={{ fontSize: '10px', color: '#f59e0b', marginTop: '2px' }}>⚠️ Threshold: &gt;2 is anomalous</div>
        </div>

        <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
          <div style={{ fontSize: '10px', color: 'var(--text-dim)', fontWeight: 700 }}>RAPID PASS-THROUGH</div>
          <div style={{ fontSize: '20px', fontWeight: 800, color: data.rapid_passthrough_detected ? '#f43f5e' : '#10b981', marginTop: '2px' }}>
            {data.rapid_passthrough_detected ? 'ACTIVE (&gt;80%)' : 'NORMAL'}
          </div>
          <div style={{ fontSize: '10px', color: 'var(--text-dim)', marginTop: '2px' }}>Layered to cash-out in &lt;15m</div>
        </div>

        <div style={{ background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
          <div style={{ fontSize: '10px', color: 'var(--text-dim)', fontWeight: 700 }}>SHARED DEVICE LINKS</div>
          <div style={{ fontSize: '20px', fontWeight: 800, color: '#c084fc', marginTop: '2px' }}>
            {data.shared_device_accounts.length} Linked Nodes
          </div>
          <div style={{ fontSize: '10px', color: 'var(--text-dim)', marginTop: '2px' }}>Hardware ID: DEV-SHARED-01</div>
        </div>
      </div>

      {/* Interactive Visual Graph Canvas */}
      <div style={{
        flex: 1,
        background: 'rgba(5, 8, 16, 0.7)',
        borderRadius: '12px',
        border: '1px solid var(--border-subtle)',
        position: 'relative',
        overflow: 'hidden',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '280px'
      }}>
        {/* Graph Nodes Layout */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '90%', position: 'relative' }}>
          {/* Victims Fan-In */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            <span style={{ fontSize: '10px', fontWeight: 700, color: 'var(--text-dim)', textAlign: 'center' }}>VICTIM REMITTERS</span>
            {['CUST-101 (Arun)', 'CUST-102 (Meera)', 'CUST-103 (Sunil)', 'CUST-104 (Pooja)'].map((victim, i) => (
              <div
                key={i}
                style={{
                  padding: '6px 12px',
                  borderRadius: '6px',
                  background: 'rgba(59, 130, 246, 0.15)',
                  border: '1px solid rgba(59, 130, 246, 0.3)',
                  fontSize: '11px',
                  fontWeight: 600,
                  color: '#93c5fd',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px'
                }}
              >
                <span>👤</span> {victim}
              </div>
            ))}
          </div>

          {/* Fan-in Arrows */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', color: 'rgba(255,255,255,0.2)' }}>
            <ArrowRight size={18} />
            <ArrowRight size={18} />
            <ArrowRight size={18} />
            <ArrowRight size={18} />
          </div>

          {/* Central Aggregator Mule Node */}
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            background: 'rgba(244, 63, 94, 0.15)',
            border: '2px solid #f43f5e',
            borderRadius: '16px',
            padding: '16px',
            boxShadow: '0 0 30px rgba(244, 63, 94, 0.35)',
            textAlign: 'center',
            minWidth: '180px'
          }}>
            <div style={{
              width: '42px',
              height: '42px',
              borderRadius: '50%',
              background: '#f43f5e',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '8px',
              boxShadow: '0 0 16px #f43f5e'
            }}>
              <AlertOctagon size={22} color="#ffffff" />
            </div>
            <div style={{ fontSize: '13px', fontWeight: 800, color: '#ffffff' }}>AGGREGATOR MULE</div>
            <div style={{ fontSize: '10px', color: '#fb7185', fontWeight: 600 }}>{data.beneficiary_id}</div>
            <span style={{ fontSize: '9px', background: 'rgba(244, 63, 94, 0.3)', padding: '2px 6px', borderRadius: '4px', marginTop: '6px' }}>
              Cluster: {data.ring_cluster_id}
            </span>
          </div>

          {/* Pass-through Arrow */}
          <div style={{ color: '#f43f5e' }}>
            <ArrowRight size={22} className="animate-pulse-slow" />
          </div>

          {/* Cash-Out & Layering Mules */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <span style={{ fontSize: '10px', fontWeight: 700, color: 'var(--text-dim)', textAlign: 'center' }}>CASHOUT / LAYERING</span>
            <div style={{
              padding: '8px 12px',
              borderRadius: '8px',
              background: 'rgba(168, 85, 247, 0.15)',
              border: '1px solid rgba(168, 85, 247, 0.4)',
              fontSize: '11px',
              color: '#d8b4fe',
              fontWeight: 600
            }}>
              💸 ATM Cash-out Mule #1
              <div style={{ fontSize: '9px', opacity: 0.8 }}>Shared Device ID: DEV-MULE-01</div>
            </div>

            <div style={{
              padding: '8px 12px',
              borderRadius: '8px',
              background: 'rgba(168, 85, 247, 0.15)',
              border: '1px solid rgba(168, 85, 247, 0.4)',
              fontSize: '11px',
              color: '#d8b4fe',
              fontWeight: 600
            }}>
              🔄 Crypto Merchant Pass-Through
              <div style={{ fontSize: '9px', opacity: 0.8 }}>Drained within 8 mins</div>
            </div>
          </div>
        </div>
      </div>

      {/* Summary Banner */}
      <div style={{ marginTop: '14px', background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '8px', borderLeft: '3px solid var(--accent-purple)' }}>
        <div style={{ fontSize: '11px', fontWeight: 700, color: '#c084fc', textTransform: 'uppercase' }}>
          MULE GRAPH REASONING TRACE
        </div>
        <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '2px', lineHeight: 1.4 }}>
          {data.summary}
        </div>
      </div>
    </div>
  );
}
