# 🛡️ Drishti: Agentic Scam & Fraud Intelligence for Banks

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Agent_Framework-Google_ADK-green)](https://github.com/google/adk)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React_18-61DAFB.svg)](https://react.dev)

> **"Stop the scam before the money moves."**  
> Advanced multi-agent defense system specifically engineered to intercept **Authorized Push Payment (APP) fraud** (Digital Arrest, Fake KYC APKs, Task Scams, Mule Syndicates) in real-time.

---

## 🎥 Full Feature Showcase Video

A complete 1600×950 high-definition walkthrough of all fraud scenarios, dual-layer interventions, interactive graph visualizers, and compliance filings is available in:

📹 **[assets/videos/drishti_showcase.mp4](assets/videos/drishti_showcase.mp4)**  
*(H.264, 1600×950, 25 fps, 3.42 MB, 52s runtime)*

---

## ⚡ Architecture Overview

```
                      INCOMING UPI / FAST PAYMENT STREAM
                                      │
                                      ▼
           ┌──────────────────────────────────────────────────────┐
           │        Layer 1: Real-time Risk Engine (<15ms)        │
           │  • Embedded ONNX/XGBoost Tabular Model               │
           │  • Sliding-Window Velocity Cache (Redis/In-Memory)   │
           │  • Scores 100% of traffic, 0 LLM cost                │
           └──────────────────────────┬───────────────────────────┘
                                      │
              ┌───────────────────────┼────────────────────────┐
              ▼                       ▼                        ▼
       Score < 0.35            0.35 <= Score <= 0.75      Score > 0.75
        [ ALLOW ]                   [ GREY ZONE ]           [ HOLD ]
       Instant Pass                   │                    Hard Freeze
                                      ▼
           ┌──────────────────────────────────────────────────────┐
           │        Layer 2: Multi-Agent Scam Shield (<3.5s)      │
           │  • Google ADK Parallel & Sequential Agent Hierarchy  │
           │  • Context Agent: Voice call telemetry, APK hijack   │
           │  • Mule Graph Agent: BigQuery fan-in & pass-through  │
           │  • Policy Agent: RBI Master Directions & FIU-IND     │
           │  • Intervention Agent: Contextual Plain-Language     │
           │    Friction Dialog (English, Hindi, Marathi)         │
           │  • Zero-Token Semantic Cache (<2ms intervention)     │
           └──────────────────────────┬───────────────────────────┘
                                      │
                                      ▼
           ┌──────────────────────────────────────────────────────┐
           │        Layer 3: Autonomous Investigator Copilot      │
           │  • Google ADK LoopAgent Case Workspace & Dossiers    │
           │  • Draft-Critic-Revise Loop for FIU-IND STR Reports  │
           │  • Principal Officer Cryptographic Verification Gate │
           │  • Core Banking Account Lien Freeze & FIU Submission │
           └──────────────────────────────────────────────────────┘
                                      │
                                      ▼
           ┌──────────────────────────────────────────────────────┐
           │        Layer 4: Adversarial Red-Team Arena           │
           │  • Self-Play Attack Probing (Obfuscated Leetspeak,   │
           │    Structured Smurfing <₹50k, Deepfake Judicial)     │
           │  • Defense Gap Reports & Automated Remediation Rules │
           └──────────────────────────────────────────────────────┘
```

---

## 🛡️ Enterprise Fraud Defense Breakthroughs

Drishti incorporates six core institutional breakthroughs addressing critical real-world payment vulnerabilities:

1. **Telemetry Proxy Imputation for iOS & Web Sandbox:**  
   When OS privacy restrictions prevent direct call or accessibility detection, Drishti imputes coercion through behavioral signals (hesitation latency, rapid clipboard paste cadences, and savings liquidation bursts).
2. **Trusted Payee Memory & 3-Grade Friction Ladder:**  
   Prevents catastrophic false positives on genuine emergency transfers (e.g., ICU deposits while on the phone with family) by grading friction from Tier 0 (silent pass) to Tier 1 (subtle chip) and Tier 2/3 (interactive safety quiz).
3. **Cold-Start Mule Anomaly Scorer:**  
   Detects freshly activated mule accounts (< 3 days old, newly bound VPAs, or student KYC receiving large corporate sums) without requiring prior transaction history.
4. **Cryptographic Informed Consent Vault & Safety Hard Block:**  
   Maintains a tamper-evident SHA-256 audit ledger of customer overrides for non-repudiation. For transactions with scam confidence $>0.85$, a non-negotiable **Safety Hard Block** locks funds under RBI consumer protection mandates.
5. **Simulated I4C NCRP / NPCI Consortium Registry:**  
   Enables privacy-preserving cross-bank threat intelligence matching via salted Bloom filters, identifying syndicated mule accounts instantly across institutions.
6. **Zero-Token Semantic Intervention Cache:**  
   Intercepts repetitive scam archetypes in $<2$ms with zero token cost, reducing LLM operational overhead by $>80\%$.

---

## 📁 Repository Structure

```
drishti/
├── assets/
│   └── videos/
│       └── drishti_showcase.mp4 # Full 1600x950 HD walkthrough video
├── backend/
│   ├── api/                     # Modular FastAPI APIRouters
│   │   ├── deps.py              # Singletons, metrics store & SSE broadcaster
│   │   ├── routes_scoring.py    # /score, /simulator/inject, /stream (SSE)
│   │   ├── routes_cases.py      # /cases, freeze, export-str, dismiss
│   │   ├── routes_consortium.py # /consortium/lookup
│   │   ├── routes_governance.py # /consent, /cache/metrics, /metrics/roi
│   │   └── schemas.py           # Pydantic API request & response contracts
│   ├── cache/                   # Semantic intervention zero-token cache
│   ├── consortium/              # I4C NCRP salted Bloom filter registry
│   ├── engine/                  # Feature pipeline, risk scorer & payee memory
│   ├── schemas/                 # Transaction & DeviceSignals models
│   ├── security/                # Informed consent vault & PII tokenizer
│   └── main.py                  # Sleek application coordinator (75 lines)
├── agents/                      # Google ADK Multi-Agent Hierarchy
│   ├── scam_shield.py           # Layer 2 Scam Shield orchestrator
│   ├── copilot.py               # Layer 3 Investigator Copilot & STR LoopAgent
│   ├── red_team.py              # Layer 4 Adversarial Red-Team agent
│   ├── policy_agent.py          # Regulatory knowledge retrieval (RBI / FIU-IND)
│   ├── intervention_agent.py    # Multilingual friction dialogs (EN, HI, MR)
│   └── tools/                   # BigQuery Parameterized Mule Graph Analytics
├── simulator/
│   └── generator.py             # UPI & APP scam scenario simulator
├── eval/
│   └── benchmark.py             # 180-scenario golden evaluation benchmark
├── infra/
│   ├── bigquery_schema.sql      # BigQuery DDL for fraud lake & mule graph
│   ├── Dockerfile               # Container packaging for Cloud Run
│   └── cloudbuild.yaml          # Google Cloud Build deployment pipeline
├── scripts/
│   └── record_showcase_mp4.py   # Automated Playwright HD showcase recorder
├── tests/
│   ├── test_*.py                # 27 fast in-memory unit tests (~2s execution)
│   └── e2e/
│       └── ui_e2e_test.py       # 10-step Playwright browser verification suite
├── web/                         # React + Vite split-screen SOC command console
│   └── src/components/
│       ├── AlertStream.jsx      # Live real-time incoming transaction feed
│       ├── CaseDossierModal.jsx # AML dossier modal with FIU-IND export
│       ├── CaseListView.jsx     # Active cases queue & freeze controls
│       ├── ConsentAuditModal.jsx# Informed Consent Vault modal
│       ├── MuleGraphViewer.jsx  # Interactive D3/SVG fraud ring visualizer
│       ├── Navbar.jsx           # Scenario selection & system telemetry
│       ├── PhoneSimulator.jsx   # Live UPI mobile app & device signals
│       ├── RedTeamArena.jsx     # Adversarial attack lab & defense reports
│       └── RoiDashboard.jsx     # Executive ROI & Latency savings dashboard
├── requirements.txt             # Pinned Python dependencies
└── .gitignore                   # Enterprise ignore rules
```

---

## 🚀 Quickstart & Demonstration

### 1. Start the Backend API (FastAPI)
```bash
# From workspace root
python -m uvicorn backend.main:app --reload --port 8000
```
- Interactive API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/v1/health`
- Real-Time SSE Stream: `http://localhost:8000/api/v1/stream`

### 2. Start the Frontend (React + Vite)
```bash
cd web
npm run dev
```
- Open `http://localhost:5173` in your browser.

---

## 🧪 Testing & Validation

```bash
# 1. Run unit test suite (all 27 tests in ~2 seconds)
python -m pytest tests/ -v

# 2. Run golden evaluation benchmark (180 scenarios)
python -m eval.benchmark

# 3. Run full Playwright browser UI E2E test
python tests/e2e/ui_e2e_test.py

# 4. Re-record high-definition MP4 showcase video
python scripts/record_showcase_mp4.py
```

### Golden Benchmark Results:
- **Total Scenarios Evaluated:** `180`
- **Scam Detection Recall:** `100.0%`
- **Scam Detection Precision:** `100.0%`
- **False Positive Friction Rate:** `0.0%` on legitimate traffic
- **Layer 1 p95 Latency:** `0.10 ms` (SLA: `< 15 ms`)
- **Layer 2 Decision Latency:** `0.11 ms`
- **Regulatory Citation Grounding:** `100.0%` (RBI Master Directions / FIU-IND)

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.  
Copyright © 2026 Nizaal Khot and Drishti Contributors.

