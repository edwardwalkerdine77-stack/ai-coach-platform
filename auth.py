import streamlit as st

# TEMP USER DATABASE (we upgrade to real DB later)
if "users" not in st.session_state:
    st.session_state.users = {}

def login_page():
    st.title("⚽ AI Coach Login")

    choice = st.radio("Login or Sign Up", ["Login", "Sign Up"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Sign Up":
        if st.button("Create Account"):
            if username in st.session_state.users:
                st.error("User already exists")
            else:
                st.session_state.users[username] = password
                st.success("Account created! Now log in")

    if choice == "Login":
        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success("Logged in!")
                st.rerun()
            else:
                st.error("Invalid login")