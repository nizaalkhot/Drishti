import React, { useState, useEffect } from 'react';
import { PhoneCall, ShieldAlert, CheckCircle2, Smartphone, AlertTriangle, Volume2, VolumeX, Activity, ClipboardPaste } from 'lucide-react';
import ConsentAuditModal from './ConsentAuditModal';
import { API_BASE } from '../config';
import { guardianVoice } from '../utils/voiceSynthesis';

export default function PhoneSimulator({ currentTransaction, onSendPayment, isProcessing, language, setLanguage }) {
  const [amount, setAmount] = useState('480000');
  const [receiverVpa, setReceiverVpa] = useState('central.escrow.mule@paytm');
  const [remark, setRemark] = useState('CBI legal clearance security deposit');
  const [isCallActive, setIsCallActive] = useState(true);
  const [callDuration, setCallDuration] = useState(52);
  const [isApkActive, setIsApkActive] = useState(false);
  const [isTremorActive, setIsTremorActive] = useState(true);
  const [clipboardSource, setClipboardSource] = useState('telegram');
  const [isVoicePlaying, setIsVoicePlaying] = useState(false);
  const [isCooldownActive, setIsCooldownActive] = useState(false);
  const [interventionOverride, setInterventionOverride] = useState(false);
  const [showConsentModal, setShowConsentModal] = useState(false);
  const [confirmedNoCoercion, setConfirmedNoCoercion] = useState(false);
  const [consentReceipt, setConsentReceipt] = useState(null);
  const [isSubmittingConsent, setIsSubmittingConsent] = useState(false);
  const [quizAnswers, setQuizAnswers] = useState({ q1: false, q2: false });

  // Cleanup voice on unmount or intervention dismiss
  useEffect(() => {
    return () => guardianVoice.stop();
  }, []);

  // Reset interventionOverride when a new transaction is loaded
  useEffect(() => {
    setInterventionOverride(false);
    setIsCooldownActive(false);
    setShowConsentModal(false);
  }, [currentTransaction?.transaction_id, currentTransaction?.id]);

  const toggleVoiceGuidance = () => {
    if (isVoicePlaying) {
      guardianVoice.stop();
      setIsVoicePlaying(false);
    } else if (activeIntervention) {
      guardianVoice.speakIntervention({
        headline: activeIntervention.headline,
        body: activeIntervention.body,
        language: language,
        onStart: () => setIsVoicePlaying(true),
        onEnd: () => setIsVoicePlaying(false)
      });
    }
  };

  const handleSeverCall = () => {
    guardianVoice.stop();
    setIsVoicePlaying(false);
    setIsCallActive(false);
    setCallDuration(0);
    setIsCooldownActive(true);
    setInterventionOverride(true);
  };

  const activeIntervention = (!interventionOverride && currentTransaction && (currentTransaction.decision === 'INTERVENE' || currentTransaction.decision === 'HOLD'))
    ? (currentTransaction.intervention || {
        headline: "CRITICAL COERCION ALERT: Transaction Hard Blocked",
        body: "Severe multi-signal coercion detected (continuous voice call, remote device access, and coercive authority narration). Customer override is prohibited under RBI guidelines.",
        primary_action: "Disconnect Call & Protect Funds",
        secondary_action: "Call 1930 Cybercrime Helpline",
        override_action: "Customer Override Prohibited"
      })
    : null;

  const handleRecordConsent = async () => {
    if (!currentTransaction) return;
    setIsSubmittingConsent(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/consent/record`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          transaction_id: currentTransaction.transaction_id,
          customer_id: "cust_phone_simulator_user",
          scam_score: currentTransaction.risk_score,
          scam_typology: currentTransaction.intervention ? "DIGITAL_ARREST_COERCION" : "HIGH_RISK_COERCION",
          confirmed_no_coercion: confirmedNoCoercion,
          biometric_auth_token: `BIO_PASS_${Date.now().toString(36).toUpperCase()}`,
          quiz_answers_passed: quizAnswers.q1 && quizAnswers.q2
        })
      });
      const data = await res.json();
      setConsentReceipt(data);
      if (data.can_proceed) {
        setTimeout(() => {
          setInterventionOverride(true);
          setShowConsentModal(false);
          setConsentReceipt(null);
        }, 1800);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmittingConsent(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setInterventionOverride(false);
    setShowConsentModal(false);
    setConsentReceipt(null);
    setQuizAnswers({ q1: false, q2: false });
    onSendPayment({
      amount: parseFloat(amount) || 1000,
      receiver_vpa: receiverVpa,
      remark: remark,
      is_call_active: isCallActive,
      call_duration: callDuration,
      accessibility_active: isApkActive,
      gyroscope_tremor_score: isTremorActive ? 0.85 : 0.0,
      clipboard_source_app: clipboardSource !== 'none' ? clipboardSource : null
    });
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      {/* Subheader */}
      <div style={{ textAlign: 'center', marginBottom: '10px' }}>
        <h3 style={{ fontSize: '13px', fontWeight: 700, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '6px', justifyContent: 'center' }}>
          <Smartphone size={15} color="var(--accent-cyan)" />
          Customer Phone (Live UPI App)
        </h3>
        <p style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
          Simulates real device sensors, telemetry & Scam Shield friction
        </p>
      </div>

      {/* Smartphone Frame */}
      <div className="phone-mockup">
        <div className="phone-screen">
          {/* Status Bar */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '7px 18px 2px',
            fontSize: '11px',
            fontWeight: 700,
            color: '#94a3b8',
            fontFamily: 'var(--font-mono)',
            zIndex: 60
          }}>
            <span>09:41</span>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ fontSize: '9px', letterSpacing: '0.04em' }}>5G</span>
              <div style={{
                width: '18px',
                height: '9px',
                border: '1px solid #94a3b8',
                borderRadius: '2px',
                padding: '1px',
                display: 'flex',
                alignItems: 'center'
              }}>
                <div style={{ width: '85%', height: '100%', background: '#10b981', borderRadius: '1px' }} />
              </div>
            </div>
          </div>

          {/* Dynamic Island */}
          <div className="phone-island">
            <div style={{ width: '7px', height: '7px', borderRadius: '50%', background: '#22c55e' }} />
            <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#1e293b' }} />
          </div>

          {/* Active Call Floating Banner */}
          {isCallActive && (
            <div style={{
              background: 'linear-gradient(135deg, rgba(220, 38, 38, 0.96) 0%, rgba(185, 28, 28, 0.96) 100%)',
              color: '#ffffff',
              padding: '24px 14px 10px 14px',
              fontSize: '11px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              boxShadow: '0 6px 16px rgba(220, 38, 38, 0.45)',
              zIndex: 40
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <div style={{
                  width: '26px',
                  height: '26px',
                  borderRadius: '50%',
                  background: 'rgba(255, 255, 255, 0.22)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: '0 0 10px rgba(255, 255, 255, 0.3)'
                }}>
                  <PhoneCall size={13} className="animate-pulse-slow" />
                </div>
                <div>
                  <div style={{ fontWeight: 800, letterSpacing: '0.03em' }} className="font-mono">
                    IN-CALL: +91 98210 44821
                  </div>
                  <div style={{ fontSize: '9px', opacity: 0.9 }}>Active: {callDuration}m • Audio Telemetry Link</div>
                </div>
              </div>

              {/* Pulsing Audio Equalizer */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '2px', height: '14px' }}>
                {[6, 14, 20, 10, 18, 8].map((h, i) => (
                  <span
                    key={i}
                    style={{
                      width: '2.5px',
                      height: `${h}px`,
                      background: '#ffffff',
                      borderRadius: '2px',
                      animation: 'call-wave 0.8s infinite ease-in-out',
                      animationDelay: `${i * 0.12}s`
                    }}
                  />
                ))}
              </div>
            </div>
          )}

          {/* UPI Banking App Top Header */}
          <div style={{
            position: 'relative',
            zIndex: 50,
            padding: isCallActive ? '10px 14px' : '26px 14px 10px',
            borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            background: 'rgba(11, 17, 32, 0.85)',
            backdropFilter: 'blur(10px)'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '7px' }}>
              <div style={{ width: '20px', height: '20px', borderRadius: '4px', background: '#dc2626', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '10px', fontWeight: 900, color: '#fff' }}>
                UPI
              </div>
              <span style={{ fontSize: '12px', fontWeight: 700, letterSpacing: '-0.01em', color: '#f8fafc' }} className="font-display">
                Axis Mobile Pay
              </span>
            </div>

            {/* Language Picker */}
            <div style={{ display: 'flex', gap: '3px' }}>
              {['en', 'hi', 'mr'].map((lang) => (
                <button
                  key={lang}
                  type="button"
                  onClick={() => setLanguage(lang)}
                  style={{
                    padding: '2px 6px',
                    fontSize: '10px',
                    borderRadius: '4px',
                    border: 'none',
                    fontWeight: 700,
                    cursor: 'pointer',
                    transition: 'all 0.15s ease',
                    background: language === lang ? 'linear-gradient(135deg, #0e7490 0%, #0891b2 100%)' : 'rgba(255, 255, 255, 0.06)',
                    color: language === lang ? '#ffffff' : 'var(--text-muted)',
                    boxShadow: language === lang ? '0 2px 6px rgba(6, 182, 212, 0.35)' : 'none'
                  }}
                >
                  {lang === 'en' ? 'EN' : lang === 'hi' ? 'हिंदी' : 'मराठी'}
                </button>
              ))}
            </div>
          </div>

          {/* Phone Screen Scrollable Content */}
          <div style={{ flex: 1, padding: '14px', overflowY: 'auto', display: 'flex', flexDirection: 'column' }}>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '12px', flex: 1 }}>
              {/* Payee Box */}
              <div style={{
                background: 'rgba(255,255,255,0.03)',
                padding: '10px',
                borderRadius: '10px',
                border: '1px solid rgba(255,255,255,0.06)'
              }}>
                <label style={{ fontSize: '10px', color: 'var(--text-dim)', fontWeight: 600, textTransform: 'uppercase' }}>
                  Paying To (Beneficiary VPA)
                </label>
                <input
                  type="text"
                  value={receiverVpa}
                  onChange={(e) => setReceiverVpa(e.target.value)}
                  style={{
                    width: '100%',
                    background: 'transparent',
                    border: 'none',
                    color: 'var(--text-main)',
                    fontSize: '13px',
                    fontWeight: 600,
                    outline: 'none',
                    marginTop: '2px'
                  }}
                />
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '4px' }}>
                  <span style={{ fontSize: '9px', padding: '1px 5px', borderRadius: '3px', background: 'rgba(245, 158, 11, 0.2)', color: '#fbbf24', fontWeight: 600 }}>
                    FIRST-TIME BENEFICIARY
                  </span>
                </div>
              </div>

              {/* Amount Box */}
              <div style={{
                background: 'rgba(255,255,255,0.03)',
                padding: '12px',
                borderRadius: '10px',
                border: '1px solid rgba(255,255,255,0.06)',
                textAlign: 'center'
              }}>
                <label style={{ fontSize: '10px', color: 'var(--text-dim)', fontWeight: 600 }}>AMOUNT (INR)</label>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '4px', marginTop: '2px' }}>
                  <span style={{ fontSize: '22px', fontWeight: 700, color: 'var(--accent-indigo)' }}>₹</span>
                  <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    style={{
                      width: '180px',
                      background: 'transparent',
                      border: 'none',
                      color: 'var(--text-main)',
                      fontSize: '26px',
                      fontWeight: 800,
                      outline: 'none',
                      textAlign: 'center'
                    }}
                  />
                </div>
                <span style={{ fontSize: '10px', color: 'var(--text-dim)' }}>
                  Baseline 30-day Avg: ₹2,500.00
                </span>
              </div>

              {/* Remarks Box */}
              <div style={{
                background: 'rgba(255,255,255,0.03)',
                padding: '10px',
                borderRadius: '10px',
                border: '1px solid rgba(255,255,255,0.06)'
              }}>
                <label style={{ fontSize: '10px', color: 'var(--text-dim)', fontWeight: 600 }}>REMARKS / PURPOSE</label>
                <input
                  type="text"
                  value={remark}
                  onChange={(e) => setRemark(e.target.value)}
                  placeholder="e.g. CBI legal clearance"
                  style={{
                    width: '100%',
                    background: 'transparent',
                    border: 'none',
                    color: 'var(--text-main)',
                    fontSize: '12px',
                    fontWeight: 500,
                    outline: 'none',
                    marginTop: '2px'
                  }}
                />
              </div>

              {/* Telemetry Signal Toggles */}
              <div style={{
                background: 'rgba(30, 41, 59, 0.4)',
                padding: '10px',
                borderRadius: '10px',
                border: '1px solid rgba(255,255,255,0.05)',
                display: 'flex',
                flexDirection: 'column',
                gap: '8px'
              }}>
                <div style={{ fontSize: '10px', fontWeight: 700, color: 'var(--text-dim)', textTransform: 'uppercase' }}>
                  DEVICE SENSORS / TELEMETRY
                </div>

                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Active Phone Call</span>
                  <input
                    type="checkbox"
                    checked={isCallActive}
                    onChange={(e) => setIsCallActive(e.target.checked)}
                    style={{ cursor: 'pointer' }}
                  />
                </div>

                {isCallActive && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontSize: '10px', color: 'var(--text-dim)' }}>Duration:</span>
                    <input
                      type="range"
                      min="5"
                      max="90"
                      value={callDuration}
                      onChange={(e) => setCallDuration(parseInt(e.target.value))}
                      style={{ flex: 1 }}
                    />
                    <span style={{ fontSize: '10px', fontWeight: 700 }}>{callDuration}m</span>
                  </div>
                )}

                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Screen Mirror / Remote APK</span>
                  <input
                    type="checkbox"
                    checked={isApkActive}
                    onChange={(e) => setIsApkActive(e.target.checked)}
                    style={{ cursor: 'pointer' }}
                  />
                </div>

                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: '11px', color: '#fca5a5', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Activity size={12} color="#f87171" />
                    Hand Tremor (Panic Biometric)
                  </span>
                  <input
                    type="checkbox"
                    checked={isTremorActive}
                    onChange={(e) => setIsTremorActive(e.target.checked)}
                    style={{ cursor: 'pointer' }}
                  />
                </div>

                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ fontSize: '11px', color: '#93c5fd', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <ClipboardPaste size={12} color="#60a5fa" />
                    Clipboard Source App
                  </span>
                  <select
                    value={clipboardSource}
                    onChange={(e) => setClipboardSource(e.target.value)}
                    style={{
                      background: 'rgba(15, 23, 42, 0.8)',
                      border: '1px solid rgba(255,255,255,0.1)',
                      color: '#ffffff',
                      fontSize: '10px',
                      borderRadius: '4px',
                      padding: '2px 4px'
                    }}
                  >
                    <option value="telegram">Telegram (Scam VIP)</option>
                    <option value="whatsapp">WhatsApp (Unknown)</option>
                    <option value="none">Normal / Typed</option>
                  </select>
                </div>
              </div>

              {/* CON 2: Tier 1 Warning Chip */}
              {currentTransaction && currentTransaction.friction_tier === 'TIER_1_CHIP' && (
                <div style={{
                  marginBottom: '10px',
                  padding: '8px 10px',
                  borderRadius: '8px',
                  background: 'rgba(245, 158, 11, 0.15)',
                  border: '1px solid rgba(245, 158, 11, 0.35)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  color: '#fbbf24',
                  fontSize: '11px'
                }}>
                  <AlertTriangle size={15} />
                  <div>
                    <strong>Advisory Notice (Tier 1):</strong> High-value transfer to verified payee. Please ensure you are not acting on unsolicited phone instructions.
                  </div>
                </div>
              )}

              {/* Pay Button */}
              <button
                type="submit"
                disabled={isProcessing}
                className="btn btn-primary"
                style={{ width: '100%', padding: '12px', marginTop: 'auto', fontSize: '14px' }}
              >
                {isProcessing ? 'Scoring via Drishti ML...' : `Pay ₹${parseFloat(amount || 0).toLocaleString('en-IN')}`}
              </button>
            </form>

            {/* Emergency Cooldown Active Banner */}
            {isCooldownActive && (
              <div style={{
                marginTop: '10px',
                padding: '10px',
                borderRadius: '8px',
                background: 'rgba(6, 182, 212, 0.15)',
                border: '1px solid rgba(6, 182, 212, 0.4)',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                color: '#67e8f9'
              }}>
                <ShieldAlert size={18} color="#22d3ee" />
                <div style={{ fontSize: '11px' }}>
                  <strong>🛡️ Drishti Shield Active: Call Severed</strong>
                  <div style={{ fontSize: '9px', opacity: 0.9 }}>
                    15-minute protective cooldown enforced. High-risk transaction blocked and victim funds secured.
                  </div>
                </div>
              </div>
            )}

            {/* Clean Transaction Status */}
            {currentTransaction && currentTransaction.decision === 'ALLOW' && (
              <div style={{
                marginTop: '10px',
                padding: '10px',
                borderRadius: '8px',
                background: 'rgba(16, 185, 129, 0.15)',
                border: '1px solid rgba(16, 185, 129, 0.3)',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                color: '#34d399'
              }}>
                <CheckCircle2 size={16} />
                <div style={{ fontSize: '11px' }}>
                  <strong>Payment Approved (Sub-15ms)</strong>
                  <div style={{ fontSize: '9px', opacity: 0.9 }}>
                    Layer 1 Tabular: {currentTransaction.layer1_latency_ms}ms • Score: {currentTransaction.risk_score}
                    {currentTransaction.telemetry_confidence < 1.0 && ` • Proxy Conf: ${(currentTransaction.telemetry_confidence * 100).toFixed(0)}%`}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* LAYER 2 CONTEXTUAL INTERVENTION & TIER 2/3 FRICTION MODAL */}
          {activeIntervention && (
            <div style={{
              position: 'absolute',
              inset: 0,
              background: 'rgba(5, 8, 16, 0.94)',
              backdropFilter: 'blur(14px)',
              padding: '24px 18px',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'center',
              zIndex: 80,
              animation: 'fadeIn 0.2s ease-in'
            }}>
              <div style={{
                background: 'rgba(30, 27, 45, 0.95)',
                borderRadius: '16px',
                padding: '18px',
                border: currentTransaction?.can_override === false ? '2px solid #ef4444' : '1px solid rgba(244, 63, 94, 0.5)',
                boxShadow: currentTransaction?.can_override === false ? '0 0 45px rgba(239, 68, 68, 0.5)' : '0 0 35px rgba(244, 63, 94, 0.35)',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: currentTransaction?.can_override === false ? '#ef4444' : '#fb7185' }}>
                    <ShieldAlert size={24} />
                    <span style={{ fontSize: '11px', fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                      {currentTransaction?.can_override === false ? 'SAFETY HARD BLOCK' : 'Drishti Scam Shield'}
                    </span>
                  </div>
                  {currentTransaction?.semantic_cache_hit && (
                    <span style={{ fontSize: '9px', padding: '2px 6px', borderRadius: '4px', background: 'rgba(16, 185, 129, 0.2)', color: '#34d399', fontWeight: 700 }}>
                      CACHE HIT (0 TOKENS)
                    </span>
                  )}
                </div>

                <h4 style={{ fontSize: '14px', fontWeight: 800, color: '#ffffff', lineHeight: 1.3 }}>
                  {activeIntervention.headline}
                </h4>

                <p style={{ fontSize: '12px', color: '#cbd5e1', lineHeight: 1.5, background: 'rgba(0,0,0,0.3)', padding: '10px', borderRadius: '8px', borderLeft: `3px solid ${currentTransaction?.can_override === false ? '#ef4444' : '#f43f5e'}` }}>
                  {activeIntervention.body}
                </p>

                {/* CON 4: HARD BLOCK NOTICE (When confidence > 0.85) */}
                {currentTransaction?.can_override === false ? (
                  <div style={{
                    padding: '10px',
                    borderRadius: '8px',
                    background: 'rgba(239, 68, 68, 0.15)',
                    border: '1px solid rgba(239, 68, 68, 0.35)',
                    color: '#fca5a5',
                    fontSize: '11px'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
                      <AlertTriangle size={14} color="#ef4444" />
                      <strong style={{ letterSpacing: '0.02em' }}>CUSTOMER OVERRIDE PROHIBITED:</strong>
                    </div>
                    Under RBI Consumer Protection guidelines, high-coercion transfers are temporarily locked. A 2-hour cooling-off window protects your funds.
                  </div>
                ) : showConsentModal ? (
                  /* CON 4: Cryptographic Informed Consent Vault Modal */
                  <ConsentAuditModal
                    confirmedNoCoercion={confirmedNoCoercion}
                    setConfirmedNoCoercion={setConfirmedNoCoercion}
                    consentReceipt={consentReceipt}
                    isSubmittingConsent={isSubmittingConsent}
                    onRecordConsent={handleRecordConsent}
                    onCancel={() => setShowConsentModal(false)}
                  />
                ) : (
                  /* CON 2: Anti-Coercion Safety Quiz (Tier 2) */
                  <div style={{
                    background: 'rgba(15, 23, 42, 0.6)',
                    padding: '8px 10px',
                    borderRadius: '8px',
                    border: '1px solid rgba(255,255,255,0.06)',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '6px'
                  }}>
                    <div style={{ fontSize: '10px', fontWeight: 700, color: '#94a3b8' }}>
                      SAFETY VERIFICATION CHECKLIST (Tier 2):
                    </div>
                    <label style={{ fontSize: '10px', color: '#cbd5e1', display: 'flex', gap: '6px', cursor: 'pointer' }}>
                      <input
                        type="checkbox"
                        checked={quizAnswers.q1}
                        onChange={(e) => setQuizAnswers(prev => ({ ...prev, q1: e.target.checked }))}
                      />
                      <span>Caller is NOT claiming to be a CBI, Police, or Court official.</span>
                    </label>
                    <label style={{ fontSize: '10px', color: '#cbd5e1', display: 'flex', gap: '6px', cursor: 'pointer' }}>
                      <input
                        type="checkbox"
                        checked={quizAnswers.q2}
                        onChange={(e) => setQuizAnswers(prev => ({ ...prev, q2: e.target.checked }))}
                      />
                      <span>Nobody told me this payment is for a "safe verification account".</span>
                    </label>
                  </div>
                )}

                {/* DRISHTI GUARDIAN: REAL-TIME CRISIS VOICE GUIDANCE */}
                <div style={{
                  background: 'rgba(14, 116, 144, 0.2)',
                  border: '1px solid rgba(6, 182, 212, 0.4)',
                  borderRadius: '10px',
                  padding: '10px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '8px'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-cyan)' }}>
                      {isVoicePlaying ? <Volume2 size={16} className="pulse" /> : <VolumeX size={16} />}
                      <span style={{ fontSize: '11px', fontWeight: 700, letterSpacing: '0.04em' }}>
                        DRISHTI GUARDIAN VOICE INTERCEPT
                      </span>
                    </div>
                    {isVoicePlaying && (
                      <span style={{ fontSize: '9px', color: '#67e8f9', fontWeight: 600 }}>
                        DISPATCH BROADCASTING...
                      </span>
                    )}
                  </div>

                  <button
                    type="button"
                    onClick={toggleVoiceGuidance}
                    style={{
                      background: isVoicePlaying ? 'rgba(239, 68, 68, 0.3)' : 'linear-gradient(135deg, #0891b2 0%, #0284c7 100%)',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      color: '#ffffff',
                      borderRadius: '6px',
                      padding: '7px 10px',
                      fontSize: '11px',
                      fontWeight: 700,
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '6px'
                    }}
                  >
                    {isVoicePlaying ? <VolumeX size={14} /> : <Volume2 size={14} />}
                    {isVoicePlaying ? "Mute Voice Intercept" : `Speak Fraud Officer Guidance (${language.toUpperCase()})`}
                  </button>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '4px' }}>
                  {/* Emergency Sever Call Button */}
                  <button
                    type="button"
                    onClick={handleSeverCall}
                    className="btn btn-danger"
                    style={{
                      width: '100%',
                      padding: '10px',
                      fontSize: '12px',
                      background: 'linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)',
                      boxShadow: '0 0 15px rgba(220, 38, 38, 0.5)',
                      fontWeight: 800
                    }}
                  >
                    🛑 Sever Call & Enforce 15-Min Shield Cooldown
                  </button>

                  {/* Secondary Helpline Action */}
                  <button
                    type="button"
                    onClick={() => alert("Connecting to National Cybercrime Helpline 1930 / Bank Fraud Desk...")}
                    className="btn btn-outline"
                    style={{ width: '100%', padding: '8px', fontSize: '11px' }}
                  >
                    {activeIntervention.secondary_action}
                  </button>

                  {/* Override Action - Only available when not hard-blocked */}
                  {currentTransaction?.can_override !== false && !showConsentModal && (
                    <button
                      type="button"
                      onClick={() => setShowConsentModal(true)}
                      style={{
                        background: 'transparent',
                        border: 'none',
                        color: 'var(--text-dim)',
                        fontSize: '10px',
                        textDecoration: 'underline',
                        cursor: 'pointer',
                        padding: '4px'
                      }}
                    >
                      {activeIntervention.override_action}
                    </button>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
