import streamlit as st
from auth import Auth

def login_section(auth: Auth):
    """
    Отображает раздел для входа пользователя.
    """
    st.sidebar.subheader("Авторизация")
    username = st.sidebar.text_input("Имя пользователя")
    password = st.sidebar.text_input("Пароль", type="password")
    if st.sidebar.button("Войти"):
        if auth.login(username, password):
            st.sidebar.success("Успешный вход!")
            st.rerun()  # Перезагрузка интерфейса
        else:
            st.sidebar.error("Неверные учетные данные.")

def logout_section(auth: Auth):
    """
    Отображает раздел для выхода пользователя.
    """
    user = st.session_state["user"]
    st.sidebar.subheader(f"Вы вошли как {user['username']}")
    if st.sidebar.button("Выйти"):
        auth.logout()
        st.experimental_rerun()  # Перезагрузка интерфейса

