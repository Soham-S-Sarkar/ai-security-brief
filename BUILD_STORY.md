# How I Built This — The Simple Version

For anyone curious about the build process.

---

## The Problem I Started With

Security analysts receive thousands of alerts
every day. Most are noise. Some are critical.
They have no time to read them all carefully.

I wanted to build an AI that could read 
each alert and produce a clear, structured 
summary — like having a senior analyst 
available instantly for every single alert.

---

## Step 1 — Teaching The AI How To Behave

The first thing I built was not code.
It was a set of instructions for the AI
called a system prompt.

Think of it like a job description for 
the AI. It tells the AI:
- What role it plays (senior security analyst)
- What format to always follow
- What it must never do (invent details)
- How to handle uncertainty (say so honestly)

This took more iteration than any 
technical step. The instructions are 
the product.

---

## Step 2 — Connecting To An AI Model

I connected my tool to an AI model 
using an API — think of this like a 
phone line between my tool and the AI.

When my tool receives an alert, it calls 
the AI via this phone line, sends the 
alert plus the instructions, and receives 
a structured brief back.

I used OpenRouter — a service that 
connects to multiple AI models — so my 
tool is not locked to one provider.

---

## Step 3 — Building The Web Interface

I built a simple web page using a tool 
called Streamlit. It has:
- A box to paste a security alert
- Sample alerts to demo instantly
- A button to generate the brief
- Colour coded severity display
- A download button for the brief
- Feedback buttons to measure quality

No HTML. No complex web development.
Just Python — a beginner-friendly 
programming language.

---

## Step 4 — Testing It Deliberately

I tested the tool three ways:

Normal alerts — does it work correctly?
Edge cases — what happens on weird inputs?
Adversarial inputs — what happens when 
I try to break it?

The adversarial test found a critical flaw.
On a vague alert with no specific details,
the AI returned Medium severity and 
Medium confidence. Both wrong.

I call this "confidence bias" — the AI 
trying to be helpful instead of honest.

I fixed it by adding a rule to the 
instructions: no specific details = 
Low confidence, always.

---

## Step 5 — Deploying It Live

I uploaded the code to GitHub — a website 
where developers share code publicly.

Then I deployed it on Streamlit Cloud — 
a free hosting service — which gave me 
a permanent public URL anyone can open.

No servers to manage. No infrastructure 
costs. A live product in under 10 minutes.

---

## What The Tech Stack Actually Is

User opens web browser
↓
Streamlit web app (the interface)
↓
Python code (the logic)
↓
OpenRouter API (the phone line to AI)
↓
LLM model (the intelligence)
↓
Structured brief returned to user

Five layers. Each one simple on its own.
Together they make a working AI product.

---

## What I Learned

1. The AI instructions matter more than 
   the code. Get the system prompt right 
   and everything else follows.

2. Testing how your AI fails is more 
   important than testing how it succeeds.

3. A working prototype tells you things 
   a document never can. Build early, 
   even if it's rough.

4. Model agnostic architecture saved me 
   when Gemini's API failed. Never 
   lock your product to one provider 
   early.

5. Deployment is simpler than it sounds.
   A live URL is always more impressive 
   than a screenshot.
