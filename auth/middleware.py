from functools import wraps
import streamlit as st
from auth.auth import Auth

def require_permission(auth: Auth, permission: str):
    """
    Декоратор для проверки прав доступа.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "user" not in st.session_state:
                st.warning("Вы не авторизованы!")
                return
            user_id = st.session_state["user"]["user_id"]
            if not auth.has_permission(user_id, permission):
                st.error("У вас нет прав для выполнения этого действия.")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator
