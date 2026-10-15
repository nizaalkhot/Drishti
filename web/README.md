# 🛡️ Drishti SOC Command Console & UPI Phone Simulator

Enterprise split-screen security operations console and live UPI mobile payment simulator for **Drishti: Agentic Scam & Fraud Intelligence for Banks**.

---

## ⚡ Overview

The Drishti web interface provides a synchronized real-time operational environment:
- **Left Pane (Mobile Phone Simulator):** Emulates victim mobile device signals including active voice call telemetry, micro-tremor biometrics (gyroscope jitter), clipboard provenance tracking (Telegram, WhatsApp, unverified SMS), interactive scam interventions (English, Hindi, Marathi), Web Speech API voice alerts, and emergency "Sever Call & 15-Minute Safety Cooldown".
- **Right Pane (Bank SOC Command Center):** Full tier-1 bank fraud control center with:
  - **Live Alert Stream:** Real-time incoming transaction event stream powered by Server-Sent Events (SSE) with ring-buffer hydration.
  - **Mule Ring Graph Intelligence:** Interactive D3/SVG graph visualizer featuring multi-hop network expansion, circular smurfing loop detection, and risk-gradient styling.
  - **AML Case Dossiers & Investigator Copilot:** Multi-agent dossier review with core banking lien account freezing, FIU-IND FINnet 2.0 XML dossier export, and ISO 20022 `camt.056` interbank payment recall dispatch.
  - **Adversarial Red-Team Arena:** Attack vector probing with closed-loop immune patch deployment and zero-token semantic cache hot-reloading.
  - **Executive ROI & Latency Dashboard:** Institutional analytics detailing prevented loss, false-positive friction rates, sub-millisecond p95 latency, and analyst hours saved.

---

## 🛠️ Tech Stack

- **Framework:** React 19 + Vite 8
- **Icons & Visuals:** Lucide React
- **Styling:** Vanilla CSS design system with dark-mode glassmorphic cyber-defense aesthetic
- **Audio:** Web Speech API (`SpeechSynthesisUtterance`) with automatic voice matching for en-IN, hi-IN, mr-IN
- **Graph Engine:** Interactive dynamic SVG/D3 force layout
- **Linter:** Oxlint

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ (tested on Node.js 25)

### Running Locally
```bash
# From within the web directory
npm.cmd install    # (or npm install)
npm.cmd run dev    # (or npm run dev)
```
The console will start at `http://localhost:5173`.

### Connecting to Backend
By default, the application connects to the Drishti backend at `http://localhost:8000`. If running on an alternate port or host, specify `window.__DRISHTI_API_BASE__` or edit `src/config.js`.

---

## 📂 Component Architecture

| Component | Path | Description |
| :--- | :--- | :--- |
| **Navbar** | `src/components/Navbar.jsx` | Scenario injector, system status indicators, and view switcher |
| **PhoneSimulator** | `src/components/PhoneSimulator.jsx` | Mobile device simulator with biometrics, audio alerts, and UPI payments |
| **AlertStream** | `src/components/AlertStream.jsx` | Real-time SSE transaction feed with auto-scroll and quick case selection |
| **CaseListView** | `src/components/CaseListView.jsx` | High-risk case queue with severity badges and dossier inspection |
| **CaseDossierModal** | `src/components/CaseDossierModal.jsx` | Detailed AML dossier, ISO 20022 recall dispatch, and FINnet 2.0 XML export |
| **MuleGraphViewer** | `src/components/MuleGraphViewer.jsx` | Multi-hop mule ring graph with circular smurfing cycle highlights |
| **RedTeamArena** | `src/components/RedTeamArena.jsx` | Adversarial attack simulator and closed-loop immune patch deployer |
| **RoiDashboard** | `src/components/RoiDashboard.jsx` | Executive ROI metrics, latency distribution, and cost savings telemetry |
| **ConsentAuditModal**| `src/components/ConsentAuditModal.jsx` | Cryptographic SHA-256 non-repudiation consent vault audit viewer |
| **Voice Synthesis** | `src/utils/voiceSynthesis.js` | Multilingual browser speech synthesizer for high-urgency friction prompts |
