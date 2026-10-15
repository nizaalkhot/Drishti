import React from 'react';
import { Activity, Smartphone, AlertOctagon, FileText, BarChart3 } from 'lucide-react';

export default function MobileBottomNav({ activeView, setActiveView, unreadAlertsCount = 0 }) {
  const tabs = [
    { id: 'command', label: 'Radar', icon: Activity, badge: unreadAlertsCount },
    { id: 'simulator', label: 'Simulator', icon: Smartphone },
    { id: 'graph', label: 'Graph', icon: AlertOctagon },
    { id: 'cases', label: 'Cases', icon: FileText },
    { id: 'roi', label: 'Metrics', icon: BarChart3 },
  ];

  return (
    <nav 
      className="mobile-bottom-nav"
      style={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: 99,
        background: 'rgba(6, 9, 17, 0.94)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)',
        borderTop: '1px solid rgba(56, 189, 248, 0.2)',
        boxShadow: '0 -4px 20px rgba(0, 0, 0, 0.7)',
        padding: '6px 10px calc(6px + env(safe-area-inset-bottom, 8px))',
        display: 'none', // Shown via CSS media query on <= 768px
        justifyContent: 'space-around',
        alignItems: 'center'
      }}
    >
      {tabs.map((tab) => {
        const Icon = tab.icon;
        const isActive = activeView === tab.id;

        return (
          <button
            key={tab.id}
            onClick={() => setActiveView(tab.id)}
            style={{
              position: 'relative',
              background: 'transparent',
              border: 'none',
              padding: '6px 10px',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '4px',
              cursor: 'pointer',
              color: isActive ? '#38bdf8' : 'var(--text-muted)',
              transition: 'all 0.15s ease',
              minWidth: '56px'
            }}
          >
            <div style={{
              position: 'relative',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '32px',
              height: '26px',
              borderRadius: '6px',
              background: isActive ? 'rgba(6, 182, 212, 0.15)' : 'transparent',
              boxShadow: isActive ? '0 0 12px rgba(6, 182, 212, 0.4)' : 'none'
            }}>
              <Icon size={18} strokeWidth={isActive ? 2.5 : 2} />
              {tab.badge > 0 && (
                <span style={{
                  position: 'absolute',
                  top: '-3px',
                  right: '-3px',
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  background: '#ef4444',
                  boxShadow: '0 0 6px #ef4444'
                }} />
              )}
            </div>
            <span style={{
              fontSize: '10px',
              fontWeight: isActive ? 700 : 500,
              letterSpacing: '-0.01em',
              fontFamily: 'var(--font-body)'
            }}>
              {tab.label}
            </span>
          </button>
        );
      })}
    </nav>
  );
}
