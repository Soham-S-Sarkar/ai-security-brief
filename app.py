
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI Security Brief Generator",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ AI Security Brief Generator")
st.markdown("""
**Built by [Soham Sarkar] — Senior PM at BT**  
Transforms raw security alerts into 
structured CISO-ready briefings in seconds.
""")

st.divider()

st.subheader("⚙️ Setup")
api_key = st.text_input(
    "Enter your OpenRouter API Key",
    type="password",
    help="Get a free key at openrouter.ai"
)

st.divider()

st.subheader("📋 Security Alert Input")

sample_alerts = {
    "Select a sample alert...": "",
    "🔴 Critical — Ransomware Detected": "Ransomware signature detected on workstation DESKTOP-HR-042 in the HR department network segment. File encryption activity observed across 3,847 files in the past 6 minutes. Lateral movement detected to file server FS-HR-01. Network isolation not yet applied.",
    "🟠 High — Suspicious Authentication": "Unusual authentication pattern detected. User account j.smith@company.com logged in from IP 185.234.219.50 (geolocation: Russia) at 03:47 UTC. This account normally authenticates from London, UK during business hours. 15 failed attempts preceded the successful login. Account has access to financial systems and customer database.",
    "🟡 Medium — Certificate Expiry": "SSL certificate for api.internal.company.com will expire in 14 days on 2026-05-23. Certificate authority: DigiCert. Affects internal API gateway used by development and staging environments only.",
    "🔴 Critical — Data Exfiltration": "Data exfiltration pattern detected from workstation DESKTOP-FIN-019 assigned to user m.chen@company.com. 2.3GB transferred to external IP 203.0.113.45 over port 443 in last 2 hours. Destination IP flagged in threat intelligence database as known data broker."
}

selected = st.selectbox(
    "Load a sample alert (optional)",
    options=list(sample_alerts.keys())
)

default_text = sample_alerts[selected]

alert_input = st.text_area(
    "Or paste your own alert here",
    value=default_text,
    height=150,
    placeholder="Paste raw security alert text here..."
)

st.divider()

generate_clicked = st.button(
    "🔍 Generate Security Brief",
    type="primary",
    use_container_width=True
)

def generate_brief(alert_text, key):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=key
    )
    system_prompt = """
    You are a senior cybersecurity analyst assistant.
    Your job is to analyse security alerts and produce
    structured briefings for security teams and CISOs.

    You must always respond in EXACTLY this format:

    SEVERITY: [Critical/High/Medium/Low]
    SUMMARY: [2 sentences maximum, plain English, no jargon]
    AFFECTED SYSTEMS: [bullet list, prefix each with -]
    RECOMMENDED ACTION: [one clear, specific sentence]
    CONFIDENCE: [High/Medium/Low]
    REASON FOR CONFIDENCE: [one sentence]

    Rules you must never break:
    - Never invent system names, IPs, or usernames
      not present in the original alert
    - Never skip any section
    - Never use jargon in the SUMMARY
    - If ambiguous, always use CONFIDENCE: Low
    """
    response = client.chat.completions.create(
        model="openrouter/auto",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",
             "content": f"Analyse this alert:\n\n{alert_text}"}
        ]
    )
    return response.choices[0].message.content

if generate_clicked:
    if not api_key:
        st.error("Please enter your OpenRouter API key above.")
    elif not alert_input:
        st.error("Please enter or select a security alert.")
    else:
        with st.spinner("Analysing alert..."):
            result = generate_brief(alert_input, api_key)
            st.divider()
            st.subheader("📊 Security Brief")
            if "SEVERITY: Critical" in result:
                st.error("🔴 SEVERITY: Critical")
            elif "SEVERITY: High" in result:
                st.warning("🟠 SEVERITY: High")
            elif "SEVERITY: Medium" in result:
                st.info("🟡 SEVERITY: Medium")
            else:
                st.success("🟢 SEVERITY: Low")
            st.code(result, language=None)
            st.download_button(
                label="📋 Download Brief",
                data=result,
                file_name="security_brief.txt",
                mime="text/plain"
            )
            st.divider()
            st.subheader("📈 Analyst Feedback")
            st.markdown("Help improve the AI — was this brief useful?")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("✅ Sent as-is")
            with col2:
                st.button("✏️ Needed editing")
            with col3:
                st.button("❌ Not useful")
            st.caption(
                "Feedback data trains future versions. "
                "North star metric: % sent as-is."
            )

st.divider()
st.markdown("""
<small>
Built as a portfolio project demonstrating 
AI product management skills.
</small>
""", unsafe_allow_html=True)
