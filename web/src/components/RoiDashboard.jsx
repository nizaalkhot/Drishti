import React from 'react';
import { BarChart3, TrendingUp, DollarSign, Clock, ShieldCheck, Zap, Layers } from 'lucide-react';

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
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '10px',
            background: 'rgba(16, 185, 129, 0.2)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '1px solid rgba(16, 185, 129, 0.4)'
          }}>
            <BarChart3 size={20} color="#10b981" />
          </div>
          <div>
            <h2 style={{ fontSize: '18px', fontWeight: 800 }}>Executive Fraud ROI & Latency Intelligence</h2>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
              Quantified Value Delivery • Cost vs Latency Optimization
            </p>
          </div>
        </div>

        <span className="badge badge-allow">
          ANNUALIZED ROI: 14.8X
        </span>
      </div>

      {/* KPI Metric Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '24px' }}>
        {/* Loss Prevented */}
        <div style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#34d399', fontSize: '11px', fontWeight: 700 }}>
            <TrendingUp size={14} /> TOTAL LOSS PREVENTED
          </div>
          <div style={{ fontSize: '24px', fontWeight: 800, color: '#f8fafc', marginTop: '6px' }}>
            ₹{(data.loss_prevented_inr / 10000000).toFixed(2)} Cr
          </div>
          <p style={{ fontSize: '10px', color: 'var(--text-dim)', marginTop: '4px' }}>
            Across {data.total_scams_prevented} intercepted APP scams
          </p>
        </div>

        {/* Catch Rate */}
        <div style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#60a5fa', fontSize: '11px', fontWeight: 700 }}>
            <ShieldCheck size={14} /> FRAUD CATCH RATE
          </div>
          <div style={{ fontSize: '24px', fontWeight: 800, color: '#f8fafc', marginTop: '6px' }}>
            {data.fraud_catch_rate_pct}%
          </div>
          <p style={{ fontSize: '10px', color: 'var(--text-dim)', marginTop: '4px' }}>
            False Positive Friction: {data.false_positive_rate_pct}%
          </p>
        </div>

        {/* Analyst Hours Saved */}
        <div style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#fbbf24', fontSize: '11px', fontWeight: 700 }}>
            <Clock size={14} /> INVESTIGATOR TIME SAVED
          </div>
          <div style={{ fontSize: '24px', fontWeight: 800, color: '#f8fafc', marginTop: '6px' }}>
            {data.investigator_hours_saved.toFixed(0)} Hours
          </div>
          <p style={{ fontSize: '10px', color: 'var(--text-dim)', marginTop: '4px' }}>
            ~2.5 hrs saved per auto-drafted STR dossier
          </p>
        </div>

        {/* Gemini Traffic Routing */}
        <div style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-subtle)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#c084fc', fontSize: '11px', fontWeight: 700 }}>
            <Layers size={14} /> GEMINI TRAFFIC SHARE
          </div>
          <div style={{ fontSize: '24px', fontWeight: 800, color: '#f8fafc', marginTop: '6px' }}>
            {data.gemini_layer2_invocation_pct}%
          </div>
          <p style={{ fontSize: '10px', color: 'var(--text-dim)', marginTop: '4px' }}>
            93.6% handled by &lt;15ms tabular engine
          </p>
        </div>
      </div>

      {/* Tiered Cost & Latency Architecture Comparison */}
      <div style={{ background: 'rgba(15, 23, 42, 0.6)', padding: '20px', borderRadius: '12px', border: '1px solid var(--border-subtle)', flex: 1 }}>
        <h3 style={{ fontSize: '14px', fontWeight: 800, marginBottom: '14px', color: '#f8fafc' }}>
          Solving "LLMs are Too Slow & Expensive for Payments"
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
          {/* Layer 1 Box */}
          <div style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '13px', fontWeight: 700, color: '#38bdf8' }}>
                Layer 1: Fast Tabular ML Path
              </span>
              <span className="badge badge-allow">&lt;15ms</span>
            </div>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '8px', lineHeight: 1.5 }}>
              Handles 100% of raw payment stream. Executes embedded ONNX/XGBoost inference over sliding-window velocity counters. Cost per 100k tx: ₹0.00 in LLM tokens.
            </p>
            <div style={{ marginTop: '12px', fontSize: '12px', color: '#cbd5e1', fontWeight: 600 }}>
              p95 Decision Latency: {data.p95_layer1_latency_ms}ms
            </div>
          </div>

          {/* Layer 2 Box */}
          <div style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '13px', fontWeight: 700, color: '#c084fc' }}>
                Layer 2: Multi-Agent Scam Shield
              </span>
              <span className="badge badge-intervene">&lt;3.5s SLA</span>
            </div>
            <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '8px', lineHeight: 1.5 }}>
              Selectively invoked on ~6% grey-zone traffic. Performs multi-agent reasoning over active phone calls, mule network graph proximity, and RBI regulations to generate conversational friction.
            </p>
            <div style={{ marginTop: '12px', fontSize: '12px', color: '#cbd5e1', fontWeight: 600 }}>
              Average Response Time: {data.avg_layer2_latency_ms}ms
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
