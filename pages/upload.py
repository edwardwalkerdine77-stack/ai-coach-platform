import streamlit as st
from analyser import VideoAnalyzer

st.title("📤 Upload Gameplay")

file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])

plan = st.selectbox("Choose Plan", ["Bronze", "Silver", "Gold"])

limits = {
    "Bronze": 120,   # seconds
    "Silver": 600,
    "Gold": 999999
}

if file:

    with open("temp.mp4", "wb") as f:
        f.write(file.read())

    st.info(f"Plan selected: {plan}")

    progress = st.progress(0)
    status = st.empty()

    result = VideoAnalyzer("temp.mp4").analyse(progress, status)

    st.success("Analysis Complete")

    # ---------------- REPORT ----------------
    st.subheader("🧠 What You Did Well")
    for x in result["coach"]["positives"]:
        st.success(x)

    st.subheader("🔴 What You Need to Improve")
    for x in result["coach"]["negatives"]:
        st.error(x)

    st.subheader("🟡 How to Improve")
    for x in result["coach"]["improvements"]:
        st.warning(x)