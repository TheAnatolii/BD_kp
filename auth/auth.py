from app.db import Database
import streamlit as st
from app.utils import get_hash

class Auth:
    RESTRICTED_TABLES = ["Users", "User_Permissions"]
    def __init__(self, db: Database):
        self.db = db

    def login(self, username: str, password: str) -> bool:
        """
        Аутентификация пользователя.
        """
        user_query = """
        SELECT user_id, username, role, hash_password
        FROM "Users"
        WHERE username = %s
        """
        user = self.db.fetch_one(user_query, (username,))
        if user and (get_hash(password) == user['hash_password']):
            # Сохранение пользователя в сессии
            st.session_state.user = {
                "user_id": user["user_id"],
                "username": user["username"],
                "role": user["role"],
            }
            return True
        return False

    def logout(self):
        """
        Выход пользователя.
        """
        if "user" in st.session_state:
            del st.session_state.user

    # def has_permission(self, user_id: int, permission: str) -> bool:
    #     """
    #     Проверка, есть ли у пользователя указанное разрешение.
    #     """
        # query = """
        # SELECT 1
        # FROM "User_Permissions"
        # WHERE user_id = %s AND permission_type = %s
        # """
        # result = self.db.fetch_one(query, (user_id, permission))
        # # st.markdown(result)
        # return bool(result)
    def has_permission(self, user_id: int, permission: str, table_name: str = None) -> bool:
        """
        Проверка, есть ли у пользователя указанное разрешение.
        """
        # Проверяем роль пользователя
        query = """
        SELECT role
        FROM "Users"
        WHERE user_id = %s
        """
        user_role = self.db.fetch_one(query, (user_id,)).get("role")

        # Обычные пользователи не могут просматривать ограниченные таблицы
        if table_name in self.RESTRICTED_TABLES and user_role == "viewer":
            return False

        # Проверяем стандартное разрешение
        query = """
        SELECT 1
        FROM "User_Permissions"
        WHERE user_id = %s AND permission_type = %s
        """
        result = self.db.fetch_one(query, (user_id, permission))
        return bool(result)
