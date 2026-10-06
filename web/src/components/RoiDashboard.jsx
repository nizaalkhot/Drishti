import React from 'react';
import { BarChart3, TrendingUp, ShieldCheck, Clock, Layers, Zap } from 'lucide-react';

export default function RoiDashboard({ metrics }) {
  const defaultMetrics = {
    total_transactions_processed: 12480,
    total_scams_prevented: 142,
    loss_prevented_inr: 42850000,
    investigator_hours_saved: 355.0,
    gemini_layer2_invocation_pct: 6.4,
    false_positive_rate_pct: 0.12,
    fraud_catch_rate_pct: 98.6,
    p95_layer1_latency_ms: 11.8,
    avg_layer2_latency_ms: 480.0
  };

  const data = metrics || defaultMetrics;

  return (
    <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '22px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '38px',
            height: '38px',
            borderRadius: '10px',
            background: 'rgba(16, 185, 129, 0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '1px solid rgba(16, 185, 129, 0.35)',
            boxShadow: '0 0 16px rgba(16, 185, 129, 0.2)'
          }}>
            <BarChart3 size={20} color="#10b981" />
          </div>
          <div>
            <h2 style={{ fontSize: '18px', fontWeight: 800, color: '#f8fafc' }} className="font-display">
              Executive Fraud ROI & Latency Intelligence
            </h2>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Quantified Value Delivery • Cost vs Latency Optimization
            </p>
          </div>
        </div>

        <span className="badge badge-allow" style={{ fontSize: '12px', padding: '5px 12px' }}>
          ANNUALIZED ROI: 14.8X
        </span>
      </div>

      {/* KPI Metric Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '24px' }}>
        {/* Loss Prevented */}
        <div className="interactive-card" style={{
          background: 'rgba(255,255,255,0.02)',
          padding: '18px',
          borderRadius: '14px',
          border: '1px solid var(--border-subtle)',
          borderTop: '3px solid #10b981'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#34d399', fontSize: '11px', fontWeight: 700 }} className="font-mono">
            <TrendingUp size={14} /> TOTAL LOSS PREVENTED
          </div>
          <div style={{ fontSize: '26px', fontWeight: 800, color: '#f8fafc', marginTop: '8px' }} className="font-mono tabular-nums">
            ₹{(data.loss_prevented_inr / 10000000).toFixed(2)} Cr
          </div>
          <p style={{ fontSize: '11px', color: 'var(--text-dim)', marginTop: '4px' }}>
            Across {data.total_scams_prevented} intercepted APP scams
          </p>
        </div>

        {/* Catch Rate */}
        <div className="interactive-card" style={{
          background: 'rgba(255,255,255,0.02)',
          padding: '18px',
          borderRadius: '14px',
          border: '1px solid var(--border-subtle)',
          borderTop: '3px solid #60a5fa'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#60a5fa', fontSize: '11px', fontWeight: 700 }} className="font-mono">
            <ShieldCheck size={14} /> FRAUD RECALL RATE
          </div>
          <div style={{ fontSize: '26px', fontWeight: 800, color: '#f8fafc', marginTop: '8px' }} className="font-mono tabular-nums">
            {data.fraud_catch_rate_pct}%
          </div>
          <p style={{ fontSize: '11px', color: 'var(--text-dim)', marginTop: '4px' }}>
            False Positive Friction: {data.false_positive_rate_pct}%
          </p>
        </div>

        {/* Analyst Hours Saved */}
        <div className="interactive-card" style={{
          background: 'rgba(255,255,255,0.02)',
          padding: '18px',
          borderRadius: '14px',
          border: '1px solid var(--border-subtle)',
          borderTop: '3px solid #f59e0b'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#fbbf24', fontSize: '11px', fontWeight: 700 }} className="font-mono">
            <Clock size={14} /> INVESTIGATOR HOURS SAVED
          </div>
          <div style={{ fontSize: '26px', fontWeight: 800, color: '#f8fafc', marginTop: '8px' }} className="font-mono tabular-nums">
            {data.investigator_hours_saved.toFixed(0)} Hrs
          </div>
          <p style={{ fontSize: '11px', color: 'var(--text-dim)', marginTop: '4px' }}>
            ~2.5 hrs saved per auto-drafted STR dossier
          </p>
        </div>

        {/* Gemini Traffic Routing */}
        <div className="interactive-card" style={{
          background: 'rgba(255,255,255,0.02)',
          padding: '18px',
          borderRadius: '14px',
          border: '1px solid var(--border-subtle)',
          borderTop: '3px solid #a855f7'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#c084fc', fontSize: '11px', fontWeight: 700 }} className="font-mono">
            <Layers size={14} /> GEMINI TRAFFIC SHARE
          </div>
          <div style={{ fontSize: '26px', fontWeight: 800, color: '#f8fafc', marginTop: '8px' }} className="font-mono tabular-nums">
            {data.gemini_layer2_invocation_pct}%
          </div>
          <p style={{ fontSize: '11px', color: 'var(--text-dim)', marginTop: '4px' }}>
            93.6% handled by &lt;15ms tabular engine
          </p>
        </div>
      </div>

      {/* Tiered Cost & Latency Architecture Comparison */}
      <div style={{
        background: 'rgba(15, 23, 42, 0.7)',
        padding: '22px',
        borderRadius: '14px',
        border: '1px solid var(--border-subtle)',
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div>
            <h3 style={{ fontSize: '15px', fontWeight: 800, color: '#f8fafc' }} className="font-display">
              Dual-Engine Latency & Token Cost Optimization
            </h3>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Sub-millisecond tabular heuristics filter 94% of traffic before LLM inference
            </p>
          </div>
          <span className="badge" style={{ background: 'rgba(99, 102, 241, 0.15)', color: '#818cf8', border: '1px solid rgba(99, 102, 241, 0.3)' }}>
            <Zap size={11} /> ZERO-BUDGET RUNTIME LEAK
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '18px' }}>
          {/* Layer 1 Box */}
          <div className="interactive-card" style={{
            background: 'rgba(255,255,255,0.02)',
            padding: '18px',
            borderRadius: '12px',
            border: '1px solid var(--border-subtle)',
            borderLeft: '4px solid #38bdf8'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '14px', fontWeight: 700, color: '#38bdf8' }} className="font-display">
                Layer 1: Fast Tabular ML Path
              </span>
              <span className="badge badge-allow">&lt;15ms SLA</span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '8px', lineHeight: 1.5 }}>
              Handles 100% of raw payment stream. Executes embedded ONNX/heuristic velocity counters. Cost per 100k transactions: ₹0.00 in LLM tokens.
            </p>
            <div style={{ marginTop: '14px', fontSize: '13px', color: '#cbd5e1', fontWeight: 600 }} className="font-mono tabular-nums">
              p95 Decision Latency: <span style={{ color: '#38bdf8' }}>{data.p95_layer1_latency_ms}ms</span>
            </div>
          </div>

          {/* Layer 2 Box */}
          <div className="interactive-card" style={{
            background: 'rgba(255,255,255,0.02)',
            padding: '18px',
            borderRadius: '12px',
            border: '1px solid var(--border-subtle)',
            borderLeft: '4px solid #c084fc'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '14px', fontWeight: 700, color: '#c084fc' }} className="font-display">
                Layer 2: Multi-Agent Scam Shield
              </span>
              <span className="badge badge-intervene">&lt;3.5s SLA</span>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '8px', lineHeight: 1.5 }}>
              Selectively invoked on ~6% grey-zone traffic. Performs multi-agent reasoning over active phone calls, mule network graph proximity, and RBI regulations.
            </p>
            <div style={{ marginTop: '14px', fontSize: '13px', color: '#cbd5e1', fontWeight: 600 }} className="font-mono tabular-nums">
              Average Response Time: <span style={{ color: '#c084fc' }}>{data.avg_layer2_latency_ms}ms</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
