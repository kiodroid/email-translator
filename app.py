import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Inbox Therapist",
    page_icon="😤",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; }

.stApp {
    background: #0a0b0f;
}
.block-container {
    padding-top: 3rem;
    max-width: 780px;
}
h1 { 
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    color: white !important;
    letter-spacing: -1px;
}
p, label, .stMarkdown p {
    color: #8892a4 !important;
}
.stTextArea textarea {
    background-color: #13151c !important;
    color: #e2e8f0 !important;
    border-radius: 14px !important;
    border: 1px solid #2a2d3a !important;
    font-size: 15px !important;
    padding: 16px !important;
    caret-color: #ff4b4b !important;
}
.stTextArea textarea:focus {
    border: 1px solid #ff4b4b !important;
    box-shadow: 0 0 0 3px rgba(255,75,75,0.15) !important;
}
.stTextArea textarea::placeholder {
    color: #3a3f52 !important;
}
.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    border: none !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #ff4b4b, #ff7a18) !important;
    color: white !important;
    padding: 0.7rem 2rem !important;
    font-size: 16px !important;
    width: 100% !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(255,75,75,0.35) !important;
}
.stButton > button[kind="secondary"] {
    background: #13151c !important;
    color: #8892a4 !important;
    border: 1px solid #2a2d3a !important;
    font-size: 13px !important;
}
.stRadio > div {
    background: #13151c;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #2a2d3a;
    gap: 8px !important;
}
.stRadio label {
    color: #c8d0de !important;
    font-size: 14px !important;
}
.stDivider {
    border-color: #1e2130 !important;
}
.result-card {
    background: #13151c;
    padding: 28px;
    border-radius: 16px;
    border: 1px solid #2a2d3a;
    margin-top: 8px;
}
.result-card strong {
    color: #e2e8f0 !important;
}
.result-card p {
    color: #c8d0de !important;
    line-height: 1.7 !important;
}
.badge-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
    margin: 16px 0;
}
.badge {
    background: #13151c;
    border: 1px solid #2a2d3a;
    color: #8892a4;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key="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")

# Header
st.markdown("""
<div style='text-align:center; padding-bottom:8px'>
    <div style='font-size:48px'>😤</div>
    <h1>Inbox Therapist</h1>
    <p style='font-size:16px; margin-top:4px'>Decode passive aggressive emails • Detect urgency • Craft perfect replies</p>
    <div class='badge-row'>
        <span class='badge'>🎭 Tone Detection</span>
        <span class='badge'>⚡ Urgency Score</span>
        <span class='badge'>🛡️ Reply Generator</span>
        <span class='badge'>🗑️ Spam Detector</span>
        <span class='badge'>🚩 Red Flag Alerts</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# Mode selector
mode = st.radio("**Choose mode:**", [
    "🔍 Decode — What does this email actually mean?",
    "🛡️ Reply — Help me respond to this",
    "⚡ Analyze — Urgency + Spam + Importance score"
])

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# Example buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("📧 Load Example 1", use_container_width=True):
        st.session_state.email_text = "Hi! Just circling back on this — no rush at all! I know you're super busy. Just want to make sure we're aligned on the timeline. Whenever you get a chance, that'd be great. Again, absolutely no rush! 😊"
with col2:
    if st.button("📧 Load Example 2", use_container_width=True):
        st.session_state.email_text = "Per my last email, as previously discussed, I wanted to make sure this didn't slip through the cracks. Going forward, please ensure timely responses."

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# Email input
email_text = st.text_area(
    "",
    value=st.session_state.get("email_text", ""),
    height=200,
    placeholder="Paste that work email here... (or load an example above)",
    label_visibility="collapsed",
    key="email_box"
)

MODE_PROMPTS = {
    "🔍 Decode — What does this email actually mean?": """You are a brutally honest corporate email translator.
Respond in EXACTLY this format, use proper line breaks between each section:

**🎭 What they said:** [quote the most passive aggressive line]

**😤 What they mean:** [brutally honest one-liner]

**🎯 What they want:** [the actual ask in plain English]

**⚠️ Threat level:** 🔴 High / 🟡 Medium / 🟢 Low — [one line why]

**💭 Unsaid:** [what they're thinking but won't type]""",

    "🛡️ Reply — Help me respond to this": """You are a professional email strategist.
Respond in EXACTLY this format:

**🧊 Safe Reply:**
[Professional and neutral — copy-paste ready]

**🔥 Firm Reply:**
[Direct and assertive — copy-paste ready]

**☢️ Nuclear Option:**
[Technically professional but devastating — copy-paste ready]

**💡 My Recommendation:** [which one and why in one line]""",

    "⚡ Analyze — Urgency + Spam + Importance score": """You are an inbox intelligence analyst.
Respond in EXACTLY this format:

**⚡ Urgency Score:** [1-10]/10 — [one line why]

**🗑️ Spam Likelihood:** Low / Medium / High — [one line why]

**📌 Importance:** Must Reply / Can Wait / Ignore — [one line why]

**🚩 Red Flags:**
- [manipulative or concerning phrase 1]
- [manipulative or concerning phrase 2]
- [manipulative or concerning phrase 3]

**📋 TL;DR:** [one sentence — what this email actually is]"""
}

if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = ""

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

if st.session_state.usage_count >= 5:
    st.markdown("""
    <div style='background:#1a0a0a; border:1px solid #3a1a1a; border-radius:12px; padding:20px; text-align:center'>
        <p style='color:#ff4b4b; font-weight:600; font-size:16px'>🚫 5 free uses done for today</p>
        <p style='color:#8892a4; font-size:14px'>Come back tomorrow for 5 more free translations</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if st.button("🔥 Analyze Email", type="primary"):
    if not email_text.strip():
        st.warning("Paste an email first!")
    else:
        with st.spinner("Decoding corporate BS..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": MODE_PROMPTS[mode]},
                    {"role": "user", "content": email_text}
                ],
                temperature=0.7,
                max_tokens=700
            )
            result = response.choices[0].message.content
            st.session_state.last_result = result
            st.session_state.usage_count += 1

if st.session_state.last_result:
    st.divider()
    st.markdown(f"""
    <div class='result-card'>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(st.session_state.last_result)
    st.caption(f"Uses today: {st.session_state.usage_count}/5 • Free forever • No signup required")

st.divider()
st.markdown("<p style='text-align:center; color:#2a2d3a; font-size:12px'>Inbox Therapist • For people who are done pretending corporate emails are fine</p>", unsafe_allow_html=True)