import React, { useState, useEffect } from 'react';
import { Download, Share, X, Shield, Smartphone } from 'lucide-react';
import { pwaManager } from '../utils/pwaManager';

export default function InstallBanner() {
  const [pwaState, setPwaState] = useState({
    isInstallable: false,
    isStandalone: false,
    isIOS: false
  });
  const [isDismissed, setIsDismissed] = useState(() => {
    return typeof window !== 'undefined' && sessionStorage.getItem('drishti_pwa_dismissed') === 'true';
  });
  const [showIOSGuide, setShowIOSGuide] = useState(false);

  useEffect(() => {
    const unsubscribe = pwaManager.subscribe((state) => {
      setPwaState(state);
    });

    return () => unsubscribe();
  }, []);

  const handleDismiss = () => {
    setIsDismissed(true);
    sessionStorage.setItem('drishti_pwa_dismissed', 'true');
  };

  const handleInstallClick = async () => {
    if (pwaState.isInstallable) {
      await pwaManager.promptInstall();
    } else if (pwaState.isIOS) {
      setShowIOSGuide(true);
    }
  };

  // If running as an installed standalone app or dismissed, hide banner
  if (pwaState.isStandalone || isDismissed) {
    return null;
  }

  // Only show if installable on Chrome/Android/Edge OR iOS Safari
  if (!pwaState.isInstallable && !pwaState.isIOS) {
    return null;
  }

  return (
    <>
      <div style={{
        position: 'relative',
        zIndex: 90,
        background: 'linear-gradient(90deg, rgba(14, 116, 144, 0.95) 0%, rgba(3, 105, 161, 0.95) 50%, rgba(67, 56, 202, 0.95) 100%)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
        borderBottom: '1px solid rgba(56, 189, 248, 0.35)',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.45)',
        padding: '8px 16px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '12px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', minWidth: 0 }}>
          <div style={{
            width: '28px',
            height: '28px',
            borderRadius: '6px',
            background: 'rgba(255, 255, 255, 0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0
          }}>
            <Shield size={16} color="#ffffff" strokeWidth={2.4} />
          </div>
          <div style={{ minWidth: 0 }}>
            <p style={{
              margin: 0,
              fontSize: '12px',
              fontWeight: 700,
              color: '#ffffff',
              letterSpacing: '-0.01em',
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis'
            }}>
              Install Drishti Mobile App
            </p>
            <p style={{
              margin: 0,
              fontSize: '11px',
              color: 'rgba(255, 255, 255, 0.8)',
              fontWeight: 500,
              whiteSpace: 'nowrap',
              overflow: 'hidden',
              textOverflow: 'ellipsis'
            }}>
              Full-screen incident command center with offline telemetry
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexShrink: 0 }}>
          <button
            onClick={handleInstallClick}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              background: '#ffffff',
              color: '#0369a1',
              border: 'none',
              padding: '5px 12px',
              borderRadius: '6px',
              fontSize: '11px',
              fontWeight: 800,
              fontFamily: 'var(--font-body)',
              cursor: 'pointer',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.25)',
              transition: 'transform 0.15s ease'
            }}
            onMouseDown={(e) => (e.currentTarget.style.transform = 'scale(0.96)')}
            onMouseUp={(e) => (e.currentTarget.style.transform = 'scale(1)')}
          >
            {pwaState.isIOS ? <Share size={13} strokeWidth={2.5} /> : <Download size={13} strokeWidth={2.5} />}
            <span>{pwaState.isIOS ? 'Install (iOS)' : 'Install App'}</span>
          </button>

          <button
            onClick={handleDismiss}
            aria-label="Dismiss banner"
            style={{
              background: 'transparent',
              border: 'none',
              color: 'rgba(255, 255, 255, 0.7)',
              cursor: 'pointer',
              padding: '4px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: '4px'
            }}
          >
            <X size={15} />
          </button>
        </div>
      </div>

      {/* iOS Safari Step-by-Step Modal */}
      {showIOSGuide && (
        <div style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(0, 0, 0, 0.75)',
          backdropFilter: 'blur(8px)',
          WebkitBackdropFilter: 'blur(8px)',
          zIndex: 1000,
          display: 'flex',
          alignItems: 'flex-end',
          justifyContent: 'center',
          padding: '16px'
        }}>
          <div style={{
            background: 'rgba(15, 23, 42, 0.98)',
            border: '1px solid rgba(56, 189, 248, 0.3)',
            borderRadius: '16px',
            padding: '20px',
            maxWidth: '380px',
            width: '100%',
            color: '#f8fafc',
            boxShadow: '0 10px 40px rgba(0, 0, 0, 0.8)',
            animation: 'slideUp 0.25s cubic-bezier(0.16, 1, 0.3, 1)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Smartphone size={18} color="#38bdf8" />
                <h4 style={{ margin: 0, fontSize: '15px', fontWeight: 800 }}>Install Drishti on iOS</h4>
              </div>
              <button
                onClick={() => setShowIOSGuide(false)}
                style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}
              >
                <X size={18} />
              </button>
            </div>

            <ol style={{
              margin: '0 0 16px',
              paddingLeft: '20px',
              fontSize: '13px',
              lineHeight: 1.6,
              color: '#cbd5e1'
            }}>
              <li style={{ marginBottom: '8px' }}>
                In Safari, tap the <strong style={{ color: '#38bdf8' }}>Share button</strong> (<span style={{ fontSize: '14px' }}>⎋</span>) at the bottom toolbar.
              </li>
              <li style={{ marginBottom: '8px' }}>
                Scroll down and select <strong style={{ color: '#38bdf8' }}>Add to Home Screen</strong> (<span style={{ fontSize: '14px' }}>⊞</span>).
              </li>
              <li>
                Tap <strong style={{ color: '#38bdf8' }}>Add</strong> in the top right corner.
              </li>
            </ol>

            <button
              onClick={() => setShowIOSGuide(false)}
              style={{
                width: '100%',
                background: 'linear-gradient(135deg, #0284c7 0%, #06b6d4 100%)',
                color: '#ffffff',
                border: 'none',
                borderRadius: '8px',
                padding: '10px',
                fontSize: '13px',
                fontWeight: 700,
                cursor: 'pointer'
              }}
            >
              Got it
            </button>
          </div>
        </div>
      )}
    </>
  );
}
