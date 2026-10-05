# 🛡️ Drishti: Agentic Scam & Fraud Intelligence for Banks

> **"Stop the scam before the money moves."**
> Advanced multi-agent defense system specifically engineered to intercept **Authorized Push Payment (APP) fraud** (Digital Arrest, Fake KYC APKs, Task Scams, Mule Rings) in real-time.

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
           │  • Context Agent: Voice call telemetry, APK hijack   │
           │  • Mule Graph Agent: BigQuery fan-in & pass-through  │
           │  • Policy Agent: RBI Master Directions & FIU-IND     │
           │  • Intervention Agent: Contextual Plain-Language     │
           │    Friction Dialog (English, Hindi, Marathi)         │
           └──────────────────────────┬───────────────────────────┘
                                      │
                                      ▼
           ┌──────────────────────────────────────────────────────┐
           │        Layer 3: Autonomous Investigator Copilot      │
           │  • Multi-Agent Case Workspace & Evidence Dossier     │
           │  • Draft-Critic-Revise Loop for FIU-IND STR Reports  │
           │  • One-Click Account Freeze & Regulatory Filing      │
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
# Run entire test suite (all 20 unit & integration tests)
python -m pytest tests/

# Run golden evaluation benchmark (100 scenarios)
python -m eval.benchmark
```

### Golden Benchmark Results:
- **Scam Detection Recall:** `98.75%`
- **Scam Detection Precision:** `100.0%`
- **False Positive Friction Rate:** `0.0%` on legitimate UPI traffic
- **Layer 1 p95 Latency:** `0.04 ms` (SLA: `< 15 ms`)
- **Regulatory Citation Grounding:** `100.0%` (RBI / FIU-IND)

---

## 📁 Repository Structure

```
drishti/
├── backend/
│   ├── api/             # API routes and SSE streaming
│   ├── engine/          # Layer 1 Tabular Scorer & Feature Pipeline
│   ├── schemas/         # Pydantic data contracts (Transaction, DeviceSignals)
│   ├── security/        # DPDP-compliant PII Tokenizer & Isolated Vault
│   └── main.py          # FastAPI application entrypoint
├── agents/
│   ├── scam_shield.py   # Layer 2 Scam Shield Multi-Agent Orchestrator
│   ├── copilot.py       # Layer 3 Investigator Copilot & STR LoopAgent
│   ├── red_team.py      # Layer 4 Adversarial Red-Team Agent
│   ├── policy_agent.py  # Regulatory knowledge retrieval (RBI / FIU-IND)
│   ├── intervention_agent.py # Contextual friction dialogs (EN, HI, MR)
│   └── tools/           # BigQuery Parameterized Mule Graph Analytics
├── simulator/
│   └── generator.py     # Synthetic UPI & APP scam scenario simulator
├── eval/
│   └── benchmark.py     # 100-scenario golden evaluation benchmark
├── infra/
│   ├── bigquery_schema.sql # BigQuery DDL for fraud lake & mule graph
│   ├── Dockerfile       # Container packaging for Cloud Run
│   └── cloudbuild.yaml  # Google Cloud Build deployment pipeline
├── web/                 # Next-gen React split-screen command console
└── tests/               # 20 automated unit & regression tests
```
