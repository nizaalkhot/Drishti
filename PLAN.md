# Drishti: Agentic Scam & Fraud Intelligence for Banks

**Tagline:** *Stop the scam before the money moves.*

## 1. The Problem

Classic fraud systems catch unauthorized transactions: stolen cards, account takeover. The fastest-growing loss category in India (UPI, digital arrest scams, fake KYC calls, investment scams, mule accounts) is **authorized push payment (APP) fraud**, where the customer themselves approves the transfer under manipulation. Rule engines and tabular ML see a legitimate device, a legitimate customer, and a valid PIN. They miss it.

Banks also lose heavily on the back end: alert queues are huge, investigators spend hours per case, and suspicious transaction reports (STRs) are written by hand.

## 2. The Solution: Three Layers, One Platform

**Layer 1: Real-time Risk Engine (the fast path, under 150 ms)**
Pub/Sub transaction stream → FastAPI on Cloud Run → velocity and behavioral features (Memorystore/Redis) → Vertex AI tabular model → score and decision (allow / step-up / hold). No LLM sits in this path.

**Layer 2: Scam Shield (the gray-zone path)**
For medium-risk transactions only, Gemini-based agents reason over context: a first-time payee, an unusual amount, a remark text, a recent call or app-install signal, and mule-graph proximity of the beneficiary. If the pattern matches a manipulation script, the customer gets a **contextual, plain-language intervention** ("You're sending ₹4.8L to a new account while on a call. Banks never ask you to move money to a 'safe account'. Pause?") instead of a generic OTP prompt. This is the core differentiator.

**Layer 3: Investigator Copilot**
A multi-agent case workspace that gathers evidence, links accounts into mule rings, checks policy, and drafts the STR with citations. A human approves.

## 3. How It Stands Out (USPs)

1. **APP-scam focus with conversational friction.** It addresses a gap that tabular fraud scores do not.
2. **Tiered cost/latency design.** ML decides in milliseconds; Gemini is invoked only on roughly 5–10% of traffic. This is the answer to "LLMs are too slow and expensive for payments."
3. **Mule-ring graph detection** in BigQuery (shared devices, beneficiaries, fan-in/fan-out patterns, rapid pass-through), surfaced visually in the console.
4. **Explainability and audit by design.** Every decision stores the features, agent reasoning trace, retrieved policy citations, and model versions. This is built for regulator and internal-audit review.
5. **Red-Team Agent (the wow factor).** An adversarial ADK agent continuously generates new scam scripts and transaction patterns against your own defenses, producing a "defense gap report" and synthetic training data. Few teams will show this.
6. **Auto-STR / compliance drafting** grounded in RBI/FIU-IND guidance through Vertex AI Search, with a mandatory human sign-off.
7. **Fraud ROI dashboard** for executives: prevented loss, false-positive friction, and analyst hours saved.

## 4. Revenue Model

- **Usage-based SaaS:** price per 1,000 scored transactions, with a premium for Layer 2 interventions.
- **Investigator Copilot seats:** per-analyst monthly pricing, with value proven by "minutes per case" reduction.
- **Compliance automation add-on:** per STR or case package.
- **Target segment:** cooperative banks, small finance banks, NBFCs and fintechs that cannot build this in-house. Large banks are a later enterprise tier.
- **Data moat (later):** a consortium network exchanging *hashed* mule and beneficiary indicators across customers, which improves with every bank onboarded.
- **Adjacent expansion:** insurance claims fraud using the same agents and Document AI.

## 5. Architecture

| Concern | Choice |
|---|---|
| Ingestion | Pub/Sub → Cloud Run (FastAPI) |
| Fast features | Memorystore (Redis) for velocity counters |
| Analytics and graph | BigQuery (transaction history, beneficiary graph tables) |
| Predictive model | Vertex AI (XGBoost/AutoML tabular), versioned, behind an endpoint |
| Agents | Google ADK with Gemini on Vertex AI (region asia-south1 where available, for data residency) |
| Documents | Document AI (KYC, bank statements, claim documents) |
| Policy RAG | Vertex AI Search over RBI circulars, internal SOPs, and scam typologies |
| App data | AlloyDB or Cloud SQL (cases, audit log, users) |
| Frontend | Next.js + React, streaming via SSE/WebSocket |
| Ops | Cloud Run, Secret Manager, Cloud Logging/Trace, OpenTelemetry |

*Note: you mentioned Google API keys. For a production-grade story, use Vertex AI with service accounts and IAM rather than API keys. For the hackathon, the Gemini API key via ADK works, but design the code so the swap is a config change.*

## 6. Agent Design (ADK)

- **Root Orchestrator:** routes the event and enforces the decision contract.
- **Context Agent:** reads transaction, remark text, customer behavior baseline, and device signals.
- **Graph/Mule Agent:** tool = parameterized BigQuery queries (no free-form SQL from the LLM).
- **Policy Agent:** tool = Vertex AI Search; returns answers with citations.
- **Intervention Agent:** writes the customer message in the right language (English/Hindi/Marathi to start) at a controlled reading level.
- **Document Agent:** Document AI wrapper plus forgery or inconsistency checks.
- **Case/STR Agent:** assembles the evidence pack and drafts the report.
- **Red-Team Agent:** offline only; generates adversarial scenarios.

ADK patterns to use: `ParallelAgent` for Context + Graph + Policy fan-out, `SequentialAgent` for the case pipeline, `LoopAgent` for draft → critic → revise on STR quality, before/after-model callbacks for guardrails and PII redaction, session state for the case context, and ADK's evaluation tooling for regression tests.

## 7. Best Practices Baked In

- **Typed contracts:** Pydantic schemas for every agent input and output; structured JSON output only.
- **Deterministic guardrails:** hard business rules (limits, sanctions hits) override the LLM.
- **Human-in-the-loop** for any irreversible action (account freeze, STR filing).
- **PII handling:** tokenize and redact before any Gemini call (Cloud DLP or custom); minimal fields only.
- **Prompt-injection defense:** transaction remarks, documents, and emails are treated as untrusted data and never as instructions; tools run with least privilege; no tool can move money.
- **Evaluation harness:** golden scenario set (precision, recall, false-positive rate, intervention quality, hallucinated-citation rate); run in CI.
- **Observability:** trace every agent step, with cost and latency per decision.
- **Idempotent, event-driven processing** with dead-letter queues; model and prompt versioning.
- **Fairness checks:** slice metrics by customer segment, region, and language so the system doesn't disproportionately block particular groups.

## 8. Arguing Against Myself (Loose Edges)

| Objection | Response |
|---|---|
| **"LLMs are too slow for payments."** | Correct, so they stay out of the auth path. ML decides fast; Gemini only handles gray-zone cases, and its fallback on timeout is the ML decision. |
| **"False positives will annoy customers and kill adoption."** | Prefer step-up and friction over blocks. Track intervention-accepted vs. overridden rates. Add a "trusted payee" memory. Report friction cost on the ROI dashboard. |
| **"You have no real bank data."** | True, and that is the biggest weakness. Use public sets (PaySim, IEEE-CIS, AML-style synthetic graphs) plus a self-built UPI-style simulator. **State plainly that metrics are on synthetic data.** Do not claim production accuracy. |
| **"Hallucinated STRs or policy citations are a compliance risk."** | Drafts only, grounded with citations; a verifier agent checks that every claim maps to evidence; a human signs. Deterministic templates for mandatory fields. |
| **"Sending customer data to an LLM violates privacy rules (DPDP, bank policy)."** | Redact and tokenize first, use regional endpoints, keep logs minimal, and offer a deployment mode where PII never leaves the bank's VPC. Have your compliance wording reviewed; I'd verify the current DPDP rules and RBI AI guidance before citing them in the pitch. |
| **"Banks won't share data in a consortium."** | Agreed; it is a Phase-3 idea, not an MVP claim. Start with single-bank value, and later exchange only hashed indicators. |
| **"Incumbents (Feedzai, FICO, Mastercard) and RBI-backed mule detection already exist."** | Position as a complement: the APP-scam intervention layer plus an investigator copilot, not a replacement score engine. Check current offerings before the pitch so the competitive slide is accurate. |
| **"Attackers will adapt to your messages."** | That is the reason for the Red-Team Agent loop and drift monitoring. |
| **"Where do the device and call signals come from?"** | In reality via the bank's mobile SDK or telecom partnerships. For the demo, simulate them and label them as assumed inputs. |
| **"Scope is too large."** | See the cut list below. |

## 9. Build Plan

**Phase 0: Foundation (about 10% of time)**
Repo (monorepo: `/backend`, `/agents`, `/web`, `/infra`, `/eval`), CI, schemas, synthetic UPI transaction simulator with injected scam and mule scenarios, BigQuery datasets.

**Phase 1: Risk Engine MVP**
Feature pipeline, Vertex AI model, FastAPI `/score` endpoint, Pub/Sub flow, a latency benchmark.

**Phase 2: Scam Shield**
Context, Graph, Policy and Intervention agents; the customer-side simulated phone UI in Next.js showing the live intervention; explanation panel.

**Phase 3: Investigator Copilot**
Case queue, mule-graph visualization, evidence pack, STR draft with citations, human approval flow, audit log.

**Phase 4: Differentiators and polish (Completed)**
Red-Team Lab, ROI dashboard, evaluation report, Hindi/Marathi interventions, Document AI KYC check.

**Phase 5: Institutional Banking & Regulatory Compliance Upgrade (Completed)**
- Behavioral biometrics (gyroscope tremor index) and telco clipboard provenance (Telegram, WhatsApp, unverified SMS).
- Autonomous closed-loop immune system: Red-Team adversarial probing with automated immunization patch synthesis and zero-token semantic cache hot-reload.
- Deep multi-hop mule ring graph intelligence with circular smurfing cycle detection and 4-hop network expansion.
- Regulatory reporting & interbank recall: FIU-IND FINnet 2.0 XML dossier export and ISO 20022 camt.056 payment cancellation recall generator with cryptographic Principal Officer signature.
- Web Speech API multilingual voice intervention warning synthesis and 15-minute emergency safety cooldown.
- Full 41-test institutional test suite and 7-phase Playwright comprehensive UI E2E automation.

## 10. Demo Script (about 5 minutes)

1. A normal payment passes in milliseconds (shows Layer 1).
2. A scam-in-progress payment is intercepted with a contextual message, biometric tremor detection, and audio alert (Layer 2).
3. The case lands in the investigator console, the mule ring lights up with circular smurfing detection, and the STR is drafted with citations (Layer 3).
4. The investigator reviews the dossier, exports the FIU-IND FINnet 2.0 XML, and dispatches an ISO 20022 camt.056 interbank payment recall.
5. The Red-Team Agent launches a novel scam script, generates an immunization patch, and hot-reloads it directly into the Layer 2 cache.
6. The executive dashboard shows loss prevented, false-positive rate, and analyst hours saved.

## 11. Success Metrics

Recall at fixed false-positive rate (100%), p95 decision latency (0.10 ms), percentage of traffic reaching Gemini, average LLM cost per decision, intervention acceptance rate, investigator minutes per case (before vs. after), citation-accuracy rate, and red-team gap closure rate.