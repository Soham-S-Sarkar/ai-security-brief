# Product Requirements Document
## AI Security Brief Generator
**Author:** [Your Name] — Senior PM at BT  
**Version:** 1.0  
**Status:** Live — Deployed May 2026  
**Live Product:** [your streamlit URL]  
**GitHub:** [your GitHub URL]  

---

## 1. Problem Statement

Security Operations Centre (SOC) analysts 
are drowning in alerts.

The average enterprise SOC receives 11,000 
alerts per day. Analysts spend 60% of their 
time reading and triaging — not responding. 
Critical threats get buried in noise.

The consequences are severe:
- Mean time to detect a breach: 204 days
- Average breach cost: $4.9 million
- Analyst turnover: 40%+ annually
  driven largely by alert fatigue

This is not a technology problem that more 
alerts will solve. It is a human capacity 
problem that AI is uniquely positioned 
to address.

---

## 2. Opportunity

AI can read, classify, and summarise 
security alerts faster and more consistently 
than any human analyst — if designed with 
the right constraints and failure modes 
accounted for.

The opportunity is not to replace analysts.
It is to give every Tier 1 analyst the 
judgment of a senior analyst, available 
instantly, on every alert, at any time.

---

## 3. Target Users

### Primary — Tier 1 Security Analyst
- Monitors 100-300 alerts per shift
- Often junior, under time pressure
- Needs: speed, clarity, confidence signal
- Pain: alert fatigue, fear of missing 
  something critical

### Secondary — CISO
- Never touches raw alerts directly
- Needs: situational awareness, narrative,
  board-ready language
- Pain: getting accurate picture without
  wading through technical noise

### Tertiary — Tier 2 Analyst
- Investigates escalations from Tier 1
- Needs: context, depth, related incidents
- Pain: time wasted on false escalations

---

## 4. Goals and Success Metrics

### Primary Goal
Reduce time from alert received to 
analyst action from 45 minutes to 
under 5 minutes.

### Success Metrics

**Model Quality**
- Severity classification accuracy: >95%
- Hallucination rate on proper nouns: 0%
- Confidence calibration: verified weekly

**Product Experience**
- Brief acceptance rate: >80%
  (sent to CISO without significant editing)
- Time to generate brief: <3 seconds
- Analyst correction rate: <20%
- Abandonment rate at AI step: <5%

**Business Impact**
- Analyst hours saved per week
- Security error rate vs pre-AI baseline
- Override rate trend: decreasing week/week

### North Star Metric
**% of AI-generated briefs sent to CISO 
without significant editing.**
Target: 80% within 90 days of launch.

---

## 5. Product Requirements

### Must Have (v1.0)
- Accept raw alert text as input
- Return structured brief in consistent format
- Classify severity: Critical/High/Medium/Low
- Provide confidence score with reasoning
- Never hallucinate proper nouns not in input
- Return CONFIDENCE: Low on vague inputs
- Generate response in under 3 seconds
- Accessible via web browser, no setup needed

### Should Have (v1.1)
- Sample alerts for instant demo
- Colour coded severity display
- Download brief as text file
- Analyst feedback buttons
- API key input without exposing credentials

### Could Have (v2.0)
- RAG layer connecting to threat intel DB
- Similar past incidents retrieval
- Estimated time to contain field
- Auto-routing to Slack/Teams/email
- SIEM integration (Chronicle, Splunk)
- Multi-language alert support

### Won't Have (v1.0)
- Automated response actions
  (human approval required for all actions)
- Storage of customer alert data
- User authentication system
- Native mobile app

---

## 6. Key Product Decisions

### Decision 1 — Confidence Score Is Mandatory
**The decision:** Every brief must include 
a confidence score. It cannot be skipped.

**Why:** In security, an AI that sounds 
equally confident whether it's right or 
wrong is more dangerous than no AI at all. 
Analysts need to know when to trust the 
output and when to investigate manually.

**The tradeoff:** Adds complexity to output.
Some users initially found it confusing.
Worth it for safety.

### Decision 2 — Minimum Evidence Threshold
**The decision:** Fewer than 3 specific 
indicators in an alert forces CONFIDENCE: Low 
and SEVERITY: Low. No exceptions.

**Why:** Discovered through adversarial 
testing. Without this rule, the model 
returned Medium severity on an alert 
containing zero specific information — 
a dangerous failure mode called 
"confidence bias."

**The tradeoff:** May frustrate users who 
want a strong answer on limited data.
The alternative — false confidence — is 
worse.

### Decision 3 — One Recommended Action Only
**The decision:** The recommended action 
field must contain exactly one sentence.

**Why:** UX research shows analysts given 
multiple options in high-stress situations 
experience decision paralysis. In security, 
paralysis costs time. Time costs money.

**The tradeoff:** Oversimplifies complex 
incidents. Accepted for v1.0 — v2.0 will 
add a secondary actions section for 
Tier 2 analysts.

### Decision 4 — Model Agnostic Architecture
**The decision:** Built on OpenRouter rather 
than a single model provider API.

**Why:** Vendor lock-in is a business risk 
for enterprise customers. During build, 
Gemini's free tier failed — switching to 
OpenRouter took 2 minutes with zero code 
change. That flexibility validated the 
architectural decision in real time.

**The tradeoff:** Less control over 
specific model behaviour. Acceptable at 
this stage.

---

## 7. What I Learned Building This

### On AI Product Design
System prompts are product decisions, not 
technical details. Every constraint written 
into the system prompt reflects a real 
user need or safety concern. The prompt 
is your product's constitution.

### On Failure Modes
The most dangerous AI failure mode is not 
obvious errors. It is confident errors on 
inputs no one thought to test. Adversarial 
testing is not optional for AI products — 
it is the most important form of QA.

### On Enterprise AI
Enterprise security customers have a 
fundamental constraint: data cannot leave 
their network. Any production version of 
this product needs a private deployment 
option — either self-hosted open source 
models or private cloud deployment via 
Vertex AI. This shapes the entire 
go-to-market strategy.

### On Metrics
High engagement can mask a broken product. 
If analysts are rubber-stamping AI outputs 
without reading them, the acceptance rate 
looks great and the product is a liability. 
Instrument explicit quality checks. Make 
trust measurable, not assumed.

---

## 8. What v2.0 Looks Like

### RAG Integration
Connect to a threat intelligence database.
When an IP appears in an alert, 
automatically retrieve its threat history.
When a malware signature is detected, 
pull related incident reports.
The brief becomes contextually rich, 
not just structurally consistent.

### The Agentic Vision
Beyond briefing — automated first response.
Low severity alerts: auto-acknowledge 
and log. Medium alerts: brief and route.
High alerts: brief, route, and notify.
Critical alerts: brief, isolate affected 
system, page incident response team.

Human approval required at each severity 
threshold. The autonomy dial is a product 
decision, not a technical one.

### SIEM Integration
Native integration with Google Chronicle,
Splunk, and Microsoft Sentinel. Alerts 
flow in automatically. Briefs flow out 
to the analyst dashboard. No manual 
copy-paste. Full audit trail.

---

## 9. Competitive Context

| Product | Strength | Gap |
|---|---|---|
| Microsoft Security Copilot | Deep Office/Azure integration | Locked to Microsoft stack |
| CrowdStrike Charlotte AI | EDR native | Narrow scope |
| Google Chronicle AI | Scale, Google infrastructure | Complex deployment |
| This tool | Lightweight, model agnostic, explainable confidence scoring | Early stage |

The gap this fills: a lightweight, 
deployable-anywhere, confidence-aware 
triage tool that works with any alert 
source and any underlying model.

---

## 10. Open Questions

1. How do we handle alerts containing 
   PII in a GDPR-compliant way?

2. At what confidence threshold should 
   the system refuse to classify and 
   escalate directly to human review?

3. Should confidence scores be shown 
   to Tier 1 analysts or only to 
   Tier 2 and above?

4. How do we prevent analysts from 
   over-relying on AI outputs as their 
   skill atrophies over time?

5. What does private deployment look 
   like for a bank or government SOC 
   where data cannot leave the building?
