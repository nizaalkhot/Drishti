import React from 'react';
import { Shield, Activity, FileText, BarChart3, AlertOctagon, Terminal } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, onInjectScenario, isInjecting, connectionStatus }) {
  return (
    <header style={{
      borderBottom: '1px solid var(--border-subtle)',
      background: 'rgba(7, 10, 18, 0.88)',
      backdropFilter: 'blur(20px)',
      WebkitBackdropFilter: 'blur(20px)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      padding: '10px 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      boxShadow: '0 4px 20px -2px rgba(0, 0, 0, 0.5)'
    }}>
      {/* Brand & Subtitle */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <div style={{
          width: '38px',
          height: '38px',
          borderRadius: '11px',
          background: 'linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 0 20px rgba(99, 102, 241, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.25)',
          border: '1px solid rgba(255, 255, 255, 0.15)'
        }}>
          <Shield size={20} color="#ffffff" strokeWidth={2.5} />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '18px', fontWeight: 800, letterSpacing: '-0.03em', color: '#f8fafc' }} className="font-display">
              DRISHTI
            </span>
            <span style={{
              fontSize: '10px',
              padding: '2px 7px',
              borderRadius: '5px',
              background: 'rgba(99, 102, 241, 0.18)',
              color: '#a5b4fc',
              fontWeight: 700,
              fontFamily: 'var(--font-mono)',
              border: '1px solid rgba(99, 102, 241, 0.35)',
              letterSpacing: '0.04em'
            }}>
              AGENTIC MESH
            </span>
          </div>
          <p style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 500 }}>
            Real-Time UPI Scam Prevention & Mule Ring Interception
          </p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <nav style={{
        display: 'flex',
        gap: '4px',
        background: 'rgba(15, 23, 42, 0.7)',
        padding: '4px',
        borderRadius: '12px',
        border: '1px solid var(--border-subtle)',
        boxShadow: 'inset 0 1px 2px rgba(0, 0, 0, 0.4)'
      }}>
        {[
          { id: 'command', label: 'Command Center', icon: Activity },
          { id: 'graph', label: 'Mule Graph', icon: AlertOctagon },
          { id: 'cases', label: 'STR Dossiers', icon: FileText },
          { id: 'redteam', label: 'Red-Team Lab', icon: Terminal },
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
                gap: '7px',
                padding: '7px 14px',
                borderRadius: '8px',
                fontFamily: 'var(--font-body)',
                fontSize: '12px',
                fontWeight: isActive ? 700 : 500,
                border: 'none',
                cursor: 'pointer',
                transition: 'all 0.18s cubic-bezier(0.16, 1, 0.3, 1)',
                background: isActive ? 'linear-gradient(135deg, #4f46e5 0%, #6366f1 100%)' : 'transparent',
                color: isActive ? '#ffffff' : 'var(--text-muted)',
                boxShadow: isActive ? '0 2px 10px rgba(99, 102, 241, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2)' : 'none'
              }}
            >
              <Icon size={14} strokeWidth={isActive ? 2.5 : 2} />
              {tab.label}
            </button>
          );
        })}
      </nav>

      {/* Scenario Launcher & Live Status */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        {/* Quick Inject Dropdown */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ fontSize: '11px', color: 'var(--text-dim)', fontWeight: 600, letterSpacing: '0.04em' }} className="font-mono">
            INJECT:
          </span>
          <select
            className="tactical-select"
            disabled={isInjecting}
            onChange={(e) => {
              if (e.target.value) {
                onInjectScenario(e.target.value);
                e.target.value = '';
              }
            }}
          >
            <option value="">⚡ Select Attack Scenario...</option>
            <option value="DIGITAL_ARREST">🛑 Digital Arrest Scam (CBI / Court)</option>
            <option value="KYC_APK_TAKEOVER">📱 Fake KYC APK / Screen Share Hijack</option>
            <option value="MULE_AGGREGATOR_FAN_IN">🕸️ Mule Aggregator Fan-In Ring</option>
            <option value="HIGH_YIELD_INVESTMENT">📈 Fake VIP Stock Trading Scam</option>
            <option value="LEGITIMATE_HOSPITAL_EMERGENCY">🏥 Hospital Emergency (Trusted Payee)</option>
            <option value="IOS_RESTRICTED_DIGITAL_ARREST">🍏 iOS Restricted (Behavioral Proxy)</option>
            <option value="FRESH_STUDENT_MULE_COLD_START">🎓 Fresh Student Mule (Cold-Start)</option>
            <option value="I4C_CONSORTIUM_SYNDICATE">🏛️ I4C Multi-Bank Registry Match</option>
            <option value="OVERRIDE_ATTEMPT_HIGH_COERCION">🔒 Coercion Override (Hard Block)</option>
            <option value="LEGITIMATE">✅ Legitimate Normal UPI Payment</option>
          </select>
        </div>

        {/* I4C Consortium & Semantic Cache Pill */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          padding: '5px 10px',
          borderRadius: '20px',
          background: 'rgba(99, 102, 241, 0.08)',
          border: '1px solid rgba(99, 102, 241, 0.22)',
          boxShadow: 'inset 0 1px 0 rgba(255, 255, 255, 0.04)'
        }}>
          <span style={{ fontSize: '10px', fontWeight: 700, color: '#a5b4fc', letterSpacing: '0.04em' }} className="font-mono">
            I4C SYNC • CACHE ON
          </span>
        </div>

        {/* Live SSE Pulse */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '7px',
          padding: '5px 12px',
          borderRadius: '20px',
          background: connectionStatus === 'connected' ? 'rgba(16, 185, 129, 0.08)' : 'rgba(245, 158, 11, 0.08)',
          border: `1px solid ${connectionStatus === 'connected' ? 'rgba(16, 185, 129, 0.25)' : 'rgba(245, 158, 11, 0.25)'}`
        }}>
          <span style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            background: connectionStatus === 'connected' ? '#10b981' : '#f59e0b',
            boxShadow: connectionStatus === 'connected' ? '0 0 10px #10b981' : '0 0 10px #f59e0b'
          }} />
          <span style={{
            fontSize: '11px',
            fontWeight: 700,
            color: connectionStatus === 'connected' ? '#34d399' : '#fbbf24',
            letterSpacing: '0.03em'
          }} className="font-mono">
            {connectionStatus === 'connected' ? 'CORE LIVE' : 'CONNECTING...'}
          </span>
        </div>
      </div>
    </header>
  );
}
