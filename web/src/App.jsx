import React, { useState, useEffect } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import PhoneSimulator from './components/PhoneSimulator';
import AlertStream from './components/AlertStream';
import MuleGraphViewer from './components/MuleGraphViewer';
import CaseDossierModal from './components/CaseDossierModal';
import CaseListView from './components/CaseListView';
import RedTeamArena from './components/RedTeamArena';
import RoiDashboard from './components/RoiDashboard';

import { API_BASE } from './config';

export default function App() {
  const [activeTab, setActiveTab] = useState('command');
  const [transactions, setTransactions] = useState([]);
  const [selectedTx, setSelectedTx] = useState(null);
  const [cases, setCases] = useState([]);
  const [selectedCase, setSelectedCase] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isInjecting, setIsInjecting] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('connecting');
  const [language, setLanguage] = useState('en');

  // Idempotent Transaction Updater to eliminate race-condition duplicates
  const upsertTransaction = (newTx) => {
    if (!newTx || !newTx.transaction_id) return;
    setTransactions(prev => {
      const idx = prev.findIndex(t => t.transaction_id === newTx.transaction_id);
      if (idx !== -1) {
        const next = [...prev];
        next[idx] = { ...next[idx], ...newTx };
        return next;
      }
      return [newTx, ...prev.slice(0, 49)];
    });
  };

  // Load Initial Cases, ROI Metrics, and Recent Ingested Transactions
  const refreshData = async () => {
    try {
      const [casesRes, metricsRes, txsRes] = await Promise.all([
        fetch(`${API_BASE}/api/v1/cases`),
        fetch(`${API_BASE}/api/v1/metrics/roi`),
        fetch(`${API_BASE}/api/v1/transactions/recent`)
      ]);
      if (casesRes.ok) {
        const casesData = await casesRes.json();
        setCases(casesData);
      }
      if (metricsRes.ok) {
        const metricsData = await metricsRes.json();
        setMetrics(metricsData);
      }
      if (txsRes.ok) {
        const txsData = await txsRes.json();
        if (Array.isArray(txsData) && txsData.length > 0) {
          setTransactions(prev => {
            if (prev.length === 0) return txsData.slice(0, 50);
            const seen = new Set(prev.map(t => t.transaction_id));
            const newFromApi = txsData.filter(t => !seen.has(t.transaction_id));
            return [...prev, ...newFromApi].slice(0, 50);
          });
          setSelectedTx(prev => prev || txsData[0]);
        }
      }
    } catch (e) {
      console.warn("Backend not yet active or offline:", e);
    }
  };

  useEffect(() => {
    void refreshData();

    // Setup SSE connection
    let eventSource;
    try {
      eventSource = new EventSource(`${API_BASE}/api/v1/stream`);
      eventSource.onopen = () => setConnectionStatus('connected');
      eventSource.onmessage = (event) => {
        try {
          const parsed = JSON.parse(event.data);
          if (parsed.type === 'TRANSACTION_SCORED') {
            upsertTransaction(parsed.data);
            setSelectedTx(parsed.data);
            refreshData();
          } else if (parsed.type === 'ACCOUNT_FROZEN' || parsed.type === 'STR_APPROVED' || parsed.type === 'CASE_DISMISSED') {
            refreshData();
          }
        } catch (err) {
          console.error("Error parsing SSE event:", err);
        }
      };
      eventSource.onerror = () => {
        setConnectionStatus('disconnected');
      };
    } catch {
      setConnectionStatus('disconnected');
    }

    return () => {
      if (eventSource) eventSource.close();
    };
  }, []);

  // Handle Quick Scenario Injection
  const handleInjectScenario = async (scenario) => {
    setIsInjecting(true);
    try {
      const res = await fetch(`${API_BASE}/api/v1/simulator/inject`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenario, language })
      });
      const data = await res.json();
      setSelectedTx(data);
      upsertTransaction(data);
      refreshData();
    } catch (e) {
      console.error(e);
      alert(`Failed to inject scenario. Ensure Drishti backend is running at ${API_BASE}`);
    } finally {
      setIsInjecting(false);
    }
  };

  // Handle Manual Payment from Customer Phone Simulator
  const handleSendPayment = async (payload) => {
    setIsProcessing(true);
    try {
      const txPayload = {
        id: `TXN-${Math.floor(100000 + Math.random() * 900000)}`,
        sender_id: "CUST-MEERA-DESHMUKH",
        sender_vpa: "meera.d@oksbi",
        sender_account: "501009821928",
        receiver_id: "MULE-AGGREGATOR-RING-1",
        receiver_vpa: payload.receiver_vpa,
        receiver_ifsc: "PYTM0123456",
        amount: payload.amount,
        remark: payload.remark,
        device: {
          device_id: "DEV-SHARED-MULE-PHONE-01",
          ip_address: "14.139.12.5",
          is_call_active: payload.is_call_active,
          call_duration_minutes: payload.call_duration,
          accessibility_service_enabled: payload.accessibility_active,
          remote_app_active: payload.accessibility_active,
          is_new_device: false,
          gyroscope_tremor_score: payload.gyroscope_tremor_score,
          clipboard_source_app: payload.clipboard_source_app
        },
        is_first_time_payee: true,
        customer_avg_tx_amount: 2500.0
      };

      const res = await fetch(`${API_BASE}/api/v1/score?language=${language}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(txPayload)
      });
      const data = await res.json();
      setSelectedTx(data);
      upsertTransaction(data);
      refreshData();
    } catch (e) {
      console.error(e);
      alert(`Failed to score transaction. Ensure backend is running at ${API_BASE}`);
    } finally {
      setIsProcessing(false);
    }
  };

  // Case Actions
  const handleFreeze = async (caseId) => {
    const res = await fetch(`${API_BASE}/api/v1/cases/${caseId}/freeze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason: "Mule Ring Aggregator Confirmed by Investigator" })
    });
    if (res.ok) {
      refreshData();
      if (selectedCase) {
        setSelectedCase(prev => ({ ...prev, status: 'ACCOUNT_FROZEN' }));
      }
    }
  };

  const handleSignSTR = async (caseId) => {
    const res = await fetch(`${API_BASE}/api/v1/cases/${caseId}/export-str`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ officer_name: "Principal Officer Sharma (AML)" })
    });
    if (res.ok) {
      const data = await res.json();
      refreshData();
      if (selectedCase) {
        setSelectedCase(prev => ({
          ...prev,
          status: 'STR_FILED',
          str_report: prev.str_report ? {
            ...prev.str_report,
            human_sign_off_status: data.human_sign_off_status || 'APPROVED_DIGITALLY_SIGNED',
            signed_by: data.signed_by,
            po_signature_hash: data.signature_hash
          } : prev.str_report
        }));
      }
    }
  };

  const handleDismiss = async (caseId) => {
    const res = await fetch(`${API_BASE}/api/v1/cases/${caseId}/dismiss`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ analyst_notes: "Customer confirmed identity via out-of-band challenge" })
    });
    if (res.ok) {
      refreshData();
      if (selectedCase) {
        setSelectedCase(prev => ({ ...prev, status: 'FALSE_POSITIVE_DISMISSED' }));
      }
    }
  };

  return (
    <div className="app-container">
      {/* Top Navigation */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onInjectScenario={handleInjectScenario}
        isInjecting={isInjecting}
        connectionStatus={connectionStatus}
      />

      {/* Main Split-Screen Workspace */}
      <main className="main-workspace">
        {/* Left Side: Bank Operations Command Center */}
        <div className="command-column">
          {activeTab === 'command' && (
            <AlertStream
              transactions={transactions}
              selectedTx={selectedTx}
              onSelectTx={(tx) => {
                setSelectedTx(tx);
                if (tx.case_id) {
                  const matched = cases.find(c => c.case_id === tx.case_id);
                  if (matched) setSelectedCase(matched);
                }
              }}
            />
          )}

          {activeTab === 'graph' && (
            <MuleGraphViewer analysis={selectedTx ? selectedTx.mule_graph_analysis : null} />
          )}

          {activeTab === 'cases' && (
            <CaseListView
              cases={cases}
              onSelectCase={(c) => setSelectedCase(c)}
            />
          )}

          {activeTab === 'redteam' && (
            <RedTeamArena />
          )}

          {activeTab === 'roi' && (
            <RoiDashboard metrics={metrics} />
          )}
        </div>

        {/* Right Side: Interactive Customer Mobile UPI Simulator */}
        <div className="simulator-column">
          <PhoneSimulator
            currentTransaction={selectedTx}
            onSendPayment={handleSendPayment}
            isProcessing={isProcessing}
            language={language}
            setLanguage={setLanguage}
          />
        </div>
      </main>

      {/* Case Dossier Modal */}
      {selectedCase && (
        <CaseDossierModal
          caseItem={selectedCase}
          onClose={() => setSelectedCase(null)}
          onFreeze={handleFreeze}
          onSignSTR={handleSignSTR}
          onDismiss={handleDismiss}
        />
      )}
    </div>
  );
}
