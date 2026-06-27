import streamlit as st
import pandas as pd
from video_analyser import VideoAnalyzer

st.set_page_config(page_title="FIFA AI Analytics", layout="wide")

st.title("⚽ Football Intelligence Platform")

file = st.file_uploader("Upload Match Video", type=["mp4", "avi", "mov"])

if file:

    with open("temp.mp4", "wb") as f:
        f.write(file.read())

    progress = st.progress(0)
    status = st.empty()

    result = VideoAnalyzer("temp.mp4").analyse(progress, status)

    st.success("Analysis Complete")

    # ---------------- TOP METRICS ----------------
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Tactical Score", f"{result['tactical_score']}/10")
    c2.metric("Pressure", result['pressure_index'])
    c3.metric("Chaos", result['chaos_index'])
    c4.metric("Events", len(result['events']))

    st.divider()

    # ---------------- MOMENTUM ----------------
    st.subheader("📈 Momentum Flow")
    st.line_chart(result["momentum"])

    st.divider()

    # ---------------- COACH ----------------
    st.subheader("🧠 AI Coach Report")

coach = result.get("coach", {
    "summary": "No analysis available",
    "positives": [],
    "negatives": [],
    "improvements": []
})

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("🟢 Strengths")
        for x in coach["positives"]:
            st.success(x)

    with col2:
        st.write("🔴 Weaknesses")
        for x in coach["negatives"]:
            st.error(x)

    with col3:
        st.write("🟡 Improvements")
        for x in coach["improvements"]:
            st.warning(x)

    st.divider()

    # ---------------- EVENTS ----------------
    st.subheader("⚽ Match Events")

    if result["events"]:
        df = pd.DataFrame(result["events"])
        st.dataframe(df, use_container_width=True)

    st.subheader("🧾 Team Identity")
    st.info(coach["identity"])