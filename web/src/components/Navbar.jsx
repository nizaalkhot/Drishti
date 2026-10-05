import React from 'react';
import { Shield, Activity, RefreshCw, Zap, Bug, FileText, BarChart3, AlertOctagon } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, onInjectScenario, isInjecting, connectionStatus }) {
  return (
    <header style={{
      borderBottom: '1px solid var(--border-subtle)',
      background: 'rgba(8, 12, 20, 0.85)',
      backdropFilter: 'blur(16px)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      padding: '12px 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between'
    }}>
      {/* Brand */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{
          width: '38px',
          height: '38px',
          borderRadius: '10px',
          background: 'linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 0 18px rgba(99, 102, 241, 0.4)'
        }}>
          <Shield size={22} color="#ffffff" />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '18px', fontWeight: 800, letterSpacing: '-0.02em' }} className="font-display">
              DRISHTI
            </span>
            <span style={{
              fontSize: '10px',
              padding: '2px 6px',
              borderRadius: '4px',
              background: 'rgba(99, 102, 241, 0.2)',
              color: '#818cf8',
              fontWeight: 700,
              border: '1px solid rgba(99, 102, 241, 0.3)'
            }}>
              AGENTIC INTELLIGENCE
            </span>
          </div>
          <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
            Stop APP Scams Before Money Moves • Team Gain
          </p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <nav style={{ display: 'flex', gap: '6px', background: 'rgba(255,255,255,0.03)', padding: '4px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
        {[
          { id: 'command', label: 'Command Center', icon: Activity },
          { id: 'graph', label: 'Mule Graph', icon: AlertOctagon },
          { id: 'cases', label: 'STR Dossiers', icon: FileText },
          { id: 'redteam', label: 'Red-Team Lab', icon: Bug },
          { id: 'roi', label: 'Executive ROI', icon: BarChart3 },
        ].map(tab => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '7px 14px',
                borderRadius: '7px',
                fontSize: '12px',
                fontWeight: 600,
                border: 'none',
                cursor: 'pointer',
                transition: 'all 0.15s ease',
                background: isActive ? 'var(--accent-indigo)' : 'transparent',
                color: isActive ? '#ffffff' : 'var(--text-muted)',
                boxShadow: isActive ? '0 2px 10px rgba(99, 102, 241, 0.4)' : 'none'
              }}
            >
              <Icon size={14} />
              {tab.label}
            </button>
          );
        })}
      </nav>

      {/* Scenario Launcher & Live Status */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        {/* Quick Inject Dropdown */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '11px', color: 'var(--text-dim)', fontWeight: 600 }}>INJECT SCENARIO:</span>
          <select
            disabled={isInjecting}
            onChange={(e) => {
              if (e.target.value) {
                onInjectScenario(e.target.value);
                e.target.value = '';
              }
            }}
            style={{
              background: 'rgba(15, 23, 42, 0.9)',
              color: 'var(--text-main)',
              border: '1px solid var(--border-subtle)',
              borderRadius: '6px',
              padding: '6px 12px',
              fontSize: '12px',
              fontWeight: 600,
              cursor: 'pointer'
            }}
          >
            <option value="">⚡ Trigger Scenario...</option>
            <option value="DIGITAL_ARREST">🛑 Digital Arrest Scam (CBI / Court)</option>
            <option value="KYC_APK_TAKEOVER">📱 Fake KYC APK / Screen Share Hijack</option>
            <option value="MULE_AGGREGATOR_FAN_IN">🕸️ Mule Aggregator Fan-In Ring</option>
            <option value="HIGH_YIELD_INVESTMENT">📈 Fake VIP Stock Trading Scam</option>
            <option value="LEGITIMATE">✅ Legitimate Normal UPI Payment</option>
          </select>
        </div>

        {/* Live SSE Pulse */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          padding: '4px 10px',
          borderRadius: '20px',
          background: connectionStatus === 'connected' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(245, 158, 11, 0.1)',
          border: `1px solid ${connectionStatus === 'connected' ? 'rgba(16, 185, 129, 0.25)' : 'rgba(245, 158, 11, 0.25)'}`
        }}>
          <span style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            background: connectionStatus === 'connected' ? '#10b981' : '#f59e0b',
            boxShadow: connectionStatus === 'connected' ? '0 0 8px #10b981' : 'none'
          }} />
          <span style={{ fontSize: '11px', fontWeight: 600, color: connectionStatus === 'connected' ? '#34d399' : '#fbbf24' }}>
            {connectionStatus === 'connected' ? 'CORE SSE LIVE' : 'CONNECTING...'}
          </span>
        </div>
      </div>
    </header>
  );
}
