import streamlit as st
from app.utils import load_env_variables
from app.db import Database
from app.pages import view_data, add_record, update_record, delete_record, upload_csv
from auth.auth import Auth

# Загрузка конфигурации
db_config = load_env_variables()
# Подключение к базе данных
db = Database(database=db_config['database'],
              host=db_config['host'],
              port=db_config['port'],
              user=db_config['user'],
              password=db_config['password'],
              min_pool=db_config['min_pool'],
              max_pool=db_config['max_pool'])
auth = Auth(db)

# Проверка аутентификации
if "user" not in st.session_state:
    st.sidebar.title("Авторизация")
    username = st.sidebar.text_input("Имя пользователя")
    password = st.sidebar.text_input("Пароль", type="password")
    if st.sidebar.button("Войти"):
        if auth.login(username, password):
            st.rerun()  # Перезапуск приложения после успешного входа
        else:
            st.sidebar.error("Неверное имя пользователя или пароль.")
    st.stop()  # Останавливаем выполнение приложения, пока пользователь не войдет в систему
else:
    user_info = st.session_state.user
    st.sidebar.title(f"Профиль: {user_info['username']}")
    if st.sidebar.button("Выйти"):
        auth.logout()
        st.rerun()  # Перезапуск приложения после выхода

# Заголовок приложения
st.title("Управление базой данных PostgreSQL")

# Меню
menu = {
    "Просмотр данных": view_data,
    "Добавить запись": add_record,
    "Обновить запись": update_record,
    "Удалить запись": delete_record,
    "Загрузить из CSV": upload_csv,
}

# Права доступа для страниц
permissions_map = {
    "Просмотр данных": "view_data",
    "Добавить запись": "add_record",
    "Обновить запись": "update_record",
    "Удалить запись": "delete_record",
    "Загрузить из CSV": "upload_csv",
}

choice = st.sidebar.radio("Выберите действие", list(menu.keys()))

# Проверка прав пользователя
current_permission = permissions_map.get(choice)
# st.markdown(current_permission)
# st.markdown(user_info["user_id"])
# st.markdown(auth.has_permission(user_info["user_id"], current_permission))
if not auth.has_permission(user_info["user_id"], current_permission):
    st.error("У вас нет прав для выполнения этого действия.")
else:
    # Переход к выбранной странице
    menu[choice].render(db, auth)
