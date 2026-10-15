import React from 'react';
import { Shield, Activity, FileText, BarChart3, AlertOctagon, Terminal } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, onInjectScenario, isInjecting, connectionStatus }) {
  return (
    <header style={{
      borderBottom: '1px solid var(--border-subtle)',
      background: 'rgba(6, 9, 17, 0.92)',
      backdropFilter: 'blur(20px)',
      WebkitBackdropFilter: 'blur(20px)',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      padding: '10px 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      boxShadow: '0 4px 24px -2px rgba(0, 0, 0, 0.6)'
    }}>
      {/* Brand & Subtitle */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        <div style={{
          width: '36px',
          height: '36px',
          borderRadius: '8px',
          background: 'linear-gradient(135deg, #0284c7 0%, #06b6d4 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 0 18px rgba(6, 182, 212, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.3)',
          border: '1px solid rgba(255, 255, 255, 0.2)'
        }}>
          <Shield size={19} color="#04121e" strokeWidth={2.6} />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '17px', fontWeight: 800, letterSpacing: '-0.03em', color: '#f8fafc' }} className="font-display">
              DRISHTI
            </span>
            <span style={{
              fontSize: '10px',
              padding: '2px 6px',
              borderRadius: '4px',
              background: 'rgba(6, 182, 212, 0.12)',
              color: '#38bdf8',
              fontWeight: 700,
              fontFamily: 'var(--font-mono)',
              border: '1px solid rgba(6, 182, 212, 0.3)',
              letterSpacing: '0.04em'
            }}>
              DEFENSE MESH
            </span>
          </div>
          <p style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 500 }}>
            Sub-Millisecond Multi-Agent Scam Prevention & Mule Ring Interception
          </p>
        </div>
      </div>

      {/* Navigation Tabs */}
      <nav className="desktop-nav" style={{
        display: 'flex',
        gap: '4px',
        background: 'rgba(11, 17, 32, 0.85)',
        padding: '3px',
        borderRadius: '8px',
        border: '1px solid var(--border-subtle)',
        boxShadow: 'inset 0 1px 2px rgba(0, 0, 0, 0.5)'
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
                padding: '6px 13px',
                borderRadius: '6px',
                fontFamily: 'var(--font-body)',
                fontSize: '12px',
                fontWeight: isActive ? 700 : 500,
                border: 'none',
                cursor: 'pointer',
                transition: 'all 0.18s cubic-bezier(0.16, 1, 0.3, 1)',
                background: isActive ? 'linear-gradient(135deg, #0e7490 0%, #0891b2 100%)' : 'transparent',
                color: isActive ? '#ffffff' : 'var(--text-muted)',
                boxShadow: isActive ? '0 2px 10px rgba(6, 182, 212, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.2)' : 'none'
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
          <span style={{ fontSize: '11px', color: 'var(--text-dim)', fontWeight: 700, letterSpacing: '0.05em' }} className="font-mono">
            INJECT:
          </span>
          <select
            className="tactical-select font-mono"
            disabled={isInjecting}
            onChange={(e) => {
              if (e.target.value) {
                onInjectScenario(e.target.value);
                e.target.value = '';
              }
            }}
          >
            <option value="">&gt;&gt; Select Attack Scenario...</option>
            <option value="DIGITAL_ARREST">[CRITICAL] Digital Arrest (CBI / Judicial Coercion)</option>
            <option value="KYC_APK_TAKEOVER">[TAKEOVER] Fake KYC APK / Remote Desktop Hijack</option>
            <option value="MULE_AGGREGATOR_FAN_IN">[MULE-RING] Mule Aggregator Rapid Fan-In</option>
            <option value="HIGH_YIELD_INVESTMENT">[INVESTMENT] VIP Trading Syndicate</option>
            <option value="LEGITIMATE_HOSPITAL_EMERGENCY">[EMERGENCY] Hospital Emergency (Trusted Payee)</option>
            <option value="IOS_RESTRICTED_DIGITAL_ARREST">[IOS-PROXY] iOS Behavioral Risk Proxy</option>
            <option value="FRESH_STUDENT_MULE_COLD_START">[COLD-START] Fresh Student Mule Account</option>
            <option value="I4C_CONSORTIUM_SYNDICATE">[CONSORTIUM] I4C Multi-Bank Registry Match</option>
            <option value="OVERRIDE_ATTEMPT_HIGH_COERCION">[HARD-BLOCK] Severe Coercion Override</option>
            <option value="LEGITIMATE">[BENIGN] Normal Legitimate UPI Transfer</option>
          </select>
        </div>

        {/* I4C Consortium & Semantic Cache Pill */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          padding: '4px 9px',
          borderRadius: '4px',
          background: 'rgba(6, 182, 212, 0.08)',
          border: '1px solid rgba(6, 182, 212, 0.22)',
          boxShadow: 'inset 0 1px 0 rgba(255, 255, 255, 0.04)'
        }}>
          <span style={{ fontSize: '10px', fontWeight: 700, color: '#38bdf8', letterSpacing: '0.05em' }} className="font-mono">
            I4C SYNC // CACHE ACTIVE
          </span>
        </div>

        {/* Live SSE Pulse */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '7px',
          padding: '4px 10px',
          borderRadius: '4px',
          background: connectionStatus === 'connected' ? 'var(--risk-allow-bg)' : 'var(--risk-intervene-bg)',
          border: `1px solid ${connectionStatus === 'connected' ? 'var(--risk-allow-border)' : 'var(--risk-intervene-border)'}`
        }}>
          <span style={{
            width: '7px',
            height: '7px',
            borderRadius: '50%',
            background: connectionStatus === 'connected' ? 'var(--risk-allow)' : 'var(--risk-intervene)',
            boxShadow: connectionStatus === 'connected' ? '0 0 8px var(--risk-allow)' : '0 0 8px var(--risk-intervene)'
          }} />
          <span style={{
            fontSize: '11px',
            fontWeight: 700,
            color: connectionStatus === 'connected' ? 'var(--risk-allow)' : 'var(--risk-intervene)',
            letterSpacing: '0.04em'
          }} className="font-mono">
            {connectionStatus === 'connected' ? 'MESH LIVE' : 'CONNECTING...'}
          </span>
        </div>
      </div>
    </header>
  );
}
