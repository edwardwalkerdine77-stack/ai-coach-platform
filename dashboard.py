import streamlit as st
import pandas as pd
from video_analyser import VideoAnalyzer
from supabase_client import supabase, get_user, create_user

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="FIFA AI Analytics", layout="wide")

# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN / SIGNUP UI ----------------
if not st.session_state.logged_in:

    st.title("⚽ FIFA AI Coach Login")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # ---------------- LOGIN ----------------
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):

            user = get_user(username)

            if user and user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    # ---------------- SIGNUP ----------------
    with tab2:
        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")

        if st.button("Create Account"):

            existing = get_user(new_user)

            if existing:
                st.error("User already exists")
            else:
                create_user(new_user, new_pass)
                st.success("Account created! Go to login.")

    st.stop()

# ---------------- LOGOUT ----------------
user = st.session_state.user

st.sidebar.title(f"👤 {user['username']}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

# ---------------- TITLE ----------------
st.title("⚽ FIFA AI Intelligence Platform")
st.markdown(f"Welcome **{user['username']}** 👋")

# ---------------- PLAN SYSTEM ----------------
plan = user.get("plan", "bronze")

st.sidebar.markdown("---")
st.sidebar.write(f"Plan: **{plan.upper()}**")

if st.sidebar.button("🥈 Upgrade to Silver"):
    supabase.table("users").update({"plan": "silver"}).eq("username", user["username"]).execute()
    user["plan"] = "silver"
    st.success("Upgraded to Silver!")
    st.rerun()

if st.sidebar.button("🥇 Upgrade to Gold"):
    supabase.table("users").update({"plan": "gold"}).eq("username", user["username"]).execute()
    user["plan"] = "gold"
    st.success("Upgraded to Gold!")
    st.rerun()

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

    # ---------------- MATCH REPORT ----------------
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
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("⚽ Tactical Score", f"{score}/10")
    c2.metric("🔥 Pressure", result["pressure_index"])
    c3.metric("💥 Chaos", result["chaos_index"])
    c4.metric("📍 Events", len(result["events"]))

    st.divider()

    # ---------------- MOMENTUM ----------------
    st.subheader("📈 Momentum Flow")
    st.line_chart(result["momentum"])

    st.divider()

    # ---------------- SCOUT REPORT ----------------
    st.subheader("🧠 AI SCOUT REPORT")

    if not FEATURES[plan]["scouting"]:
        st.warning("🔒 Upgrade to Gold to unlock Scout Report")

    else:
        scout = result.get("scout_report", {
            "rating": 0,
            "role": "Unknown",
            "strengths": [],
            "weaknesses": [],
            "improvements": []
        })

        st.markdown(f"""
        <div style="
            padding: 25px;
            border-radius: 16px;
            background: #1c1f2a;
            border: 1px solid #2d6cff;
        ">
            <h2>🎴 FIFA SCOUT CARD</h2>
            <h3 style="color:#2d6cff;">OVR: {scout['rating']}</h3>
            <p>Role: {scout['role']}</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("🟢 Strengths")
            for x in scout["strengths"]:
                st.success(x)

        with col2:
            st.write("🔴 Weaknesses")
            for x in scout["weaknesses"]:
                st.error(x)

        with col3:
            st.write("🟡 Improvements")
            for x in scout["improvements"]:
                st.warning(x)

    st.divider()

    # ---------------- EVENTS ----------------
    st.subheader("⚽ Match Events")

    if result["events"]:
        df = pd.DataFrame(result["events"])
        st.dataframe(df, use_container_width=True)