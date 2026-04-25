import streamlit as st

def login():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False

    st.sidebar.title("Login")

    usuario = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")

    if st.sidebar.button("Ingresar"):
        USER = st.secrets["USER"]
        PASS = st.secrets["PASS"]

        if usuario == USER and password == PASS:
            st.session_state["auth"] = True
        else:
            st.session_state["auth"] = False
            st.sidebar.error("Credenciales incorrectas")

    return st.session_state["auth"]