import streamlit as st
import pandas as pd
from video_analyser import VideoAnalyzer

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="FIFA AI Analytics", layout="wide")

# ---------------- 🎨 PREMIUM UI ----------------
st.markdown("""
<style>

/* BACKGROUND */
.main {
    background: radial-gradient(circle at top, #121826, #0f1117);
}

/* TEXT */
h1, h2, h3 {
    color: white;
    font-weight: 700;
}

/* METRIC CARDS */
div[data-testid="metric-container"] {
    background: rgba(28, 31, 42, 0.75);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    backdrop-filter: blur(10px);
    transition: 0.2s ease;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    border: 1px solid #2d6cff;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #0b0d12;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(90deg, #2d6cff, #6c5ce7);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 8px 14px;
    font-weight: 600;
}

.stButton > button:hover {
    transform: scale(1.03);
}

/* UPLOAD */
.css-1cpxqw2 {
    border: 1px dashed rgba(255,255,255,0.25);
    border-radius: 12px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div style="
    padding: 30px;
    border-radius: 16px;
    background: linear-gradient(135deg, #1c1f2a, #0f1117);
    border: 1px solid rgba(45,108,255,0.3);
    margin-bottom: 20px;
">
<h1>⚽ FIFA AI Intelligence Platform</h1>
<p style="color:#b0b0b0;">
EA FC-style tactical analysis • scouting reports • AI performance insights
</p>
</div>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div style="
    padding: 20px;
    border-radius: 12px;
    background-color: #1c1f2a;
    margin-bottom: 20px;
    border-left: 4px solid #2d6cff;
">
<h2>🎮 AI COACH SYSTEM</h2>
<p style="color:#b0b0b0;">
Upload your match → receive pro-level tactical breakdown + FIFA-style scouting report.
</p>
</div>
""", unsafe_allow_html=True)

# ---------------- HOW IT WORKS ----------------
st.markdown("## 🧠 How it works")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("1️⃣ Upload match footage")

with c2:
    st.info("2️⃣ AI analyses movement & pressure")

with c3:
    st.info("3️⃣ Get coaching insights")

st.markdown("## 💎 Features")

st.markdown("""
- ⚽ Tactical breakdown  
- 🧠 AI scouting report  
- 📊 Pressure + chaos metrics  
- 📈 Momentum analysis  
- 🎮 FIFA-style player ratings  
""")

# ---------------- SAAS SYSTEM ----------------
if "plan" not in st.session_state:
    st.session_state.plan = "bronze"

st.sidebar.title("⚽ AI Coach System")

st.sidebar.write(f"Plan: **{st.session_state.plan.upper()}**")
st.sidebar.markdown("---")

if st.sidebar.button("🥈 Upgrade to Silver"):
    st.session_state.plan = "silver"

if st.sidebar.button("🥇 Upgrade to Gold"):
    st.session_state.plan = "gold"

st.sidebar.markdown("---")
st.sidebar.info("Unlock scouting + full AI analysis + premium insights")

# ---------------- FEATURES ----------------
FEATURES = {
    "bronze": {"scouting": False},
    "silver": {"scouting": False},
    "gold": {"scouting": True}
}

# ---------------- UPLOAD ----------------
st.markdown("## 🎬 Upload Match Video")
file = st.file_uploader("", type=["mp4", "avi", "mov"])

if file:

    with open("temp.mp4", "wb") as f:
        f.write(file.read())

    progress = st.progress(0)
    status = st.empty()

    result = VideoAnalyzer("temp.mp4").analyse(progress, status)

    st.success("Analysis Complete")

    # ---------------- MATCH RESULT ----------------
    st.markdown("## ⚽ Match Performance Report")

    score = result["tactical_score"]

    if score >= 8:
        st.success("🟢 ELITE PERFORMANCE")
    elif score >= 6:
        st.warning("🟡 AVERAGE PERFORMANCE")
    else:
        st.error("🔴 NEEDS IMPROVEMENT")

    st.progress(score / 10)

    st.divider()

    # ---------------- METRICS ----------------
    st.markdown("## 📊 Performance Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("⚽ Tactical Score", f"{result['tactical_score']}/10")
    c2.metric("🔥 Pressure", result["pressure_index"])
    c3.metric("💥 Chaos", result["chaos_index"])
    c4.metric("📍 Events", len(result["events"]))

    st.divider()

    # ---------------- MOMENTUM ----------------
    st.subheader("📈 Momentum Flow")
    st.line_chart(result["momentum"])

    st.divider()

    # ---------------- 🧠 FIFA PLAYER CARDS (SCOUT REPORT) ----------------
    st.subheader("🧠 AI SCOUT REPORT")

    if not FEATURES[st.session_state.plan]["scouting"]:
        st.warning("🔒 Upgrade to Gold to unlock Scout Report")

    else:
        scout = result.get("scout_report", {
            "rating": 0,
            "role": "Unknown",
            "strengths": [],
            "weaknesses": [],
            "improvements": []
        })

        # ---------------- CARD HEADER ----------------
        st.markdown(f"""
        <div style="
            padding: 25px;
            border-radius: 16px;
            background: linear-gradient(135deg, #1c1f2a, #0f1117);
            border: 1px solid rgba(45,108,255,0.4);
            margin-bottom: 20px;
        ">
            <h2>🎴 FIFA SCOUT CARD</h2>
            <h3 style="color:#2d6cff;">OVR Rating: {scout['rating']}</h3>
            <p style="color:#b0b0b0;">Role: {scout['role']}</p>
        </div>
        """, unsafe_allow_html=True)

        # ---------------- 3 COLUMNS ----------------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🟢 Strengths")
            for x in scout["strengths"]:
                st.success(f"⚡ {x}")

        with col2:
            st.markdown("### 🔴 Weaknesses")
            for x in scout["weaknesses"]:
                st.error(f"⚠️ {x}")

        with col3:
            st.markdown("### 🟡 Improvements")
            for x in scout["improvements"]:
                st.warning(f"📈 {x}")

        # ---------------- INSIGHT BOX ----------------
        st.markdown("""
        <div style="
            margin-top: 20px;
            padding: 15px;
            border-radius: 12px;
            background: rgba(28,31,42,0.6);
            border-left: 4px solid #2d6cff;
        ">
        <h4>🧠 AI Tactical Insight</h4>
        <p style="color:#b0b0b0;">
        This analysis is based on motion tracking, pressure dynamics, and tactical AI modelling.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ---------------- EVENTS ----------------
    st.subheader("⚽ Match Events")

    if result["events"]:
        df = pd.DataFrame(result["events"])
        st.dataframe(df, use_container_width=True)