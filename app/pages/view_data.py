import streamlit as st
import pandas as pd


# def render(db, auth):
#     """Страница просмотра данных."""
#     st.subheader("Просмотр данных таблицы")
#
#     # Запрашиваем имя таблицы
#     table_name = st.text_input("Введите имя таблицы")
#
#     if st.button("Показать данные"):
#         try:
#             # Проверяем доступ пользователя к просмотру данных из указанной таблицы
#             user_id = st.session_state.user["user_id"]
#             if not auth.has_permission(user_id, f"view_data"):
#                 st.error("У вас нет прав для просмотра данных этой таблицы.")
#                 return
#
#             # Получаем данные из таблицы
#             data = db.fetch_all(table_name)
#             if data:
#                 df = pd.DataFrame(data)
#                 st.dataframe(df)
#             else:
#                 st.warning(f"Таблица `{table_name}` пуста или не существует.")
#         except Exception as e:
#             st.error(f"Ошибка загрузки данных: {e}")

# def render(db, auth):
#     """Страница просмотра данных таблицы."""
#     st.subheader("Просмотр данных таблицы")
#
#     # Запрашиваем имя таблицы
#     table_name = st.text_input("Введите имя таблицы")
#
#     if st.button("Показать данные"):
#         try:
#             # Проверяем доступ пользователя к просмотру данных из указанной таблицы
#             user_id = st.session_state.user["user_id"]
#             if not auth.has_permission(user_id, "view_data"):
#                 st.error("У вас нет прав для просмотра данных этой таблицы.")
#                 return
#
#             # Получаем данные из основной таблицы
#             data = db.fetch_joined_data(table_name)
#             if data:
#                 df = pd.DataFrame(data)
#                 st.dataframe(df)
#             else:
#                 st.warning(f"Таблица `{table_name}` пуста или не существует.")
#         except Exception as e:
#             st.error(f"Ошибка загрузки данных: {e}")

def render(db, auth):
    """Страница просмотра данных таблицы."""
    st.subheader("Просмотр данных таблицы")

    # Запрашиваем имя таблицы
    table_name = st.text_input("Введите имя таблицы")
    # Проверяем доступ пользователя к просмотру данных из указанной таблицы
    user_id = st.session_state.user["user_id"]
    if not auth.has_permission(user_id, "view_data", table_name):
        st.error("У вас нет прав для просмотра данных этой таблицы.")
        return

    if st.button("Показать данные"):
        try:

            # Получаем данные из основной таблицы
            data = db.fetch_joined_data(table_name)
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.warning(f"Таблица `{table_name}` пуста или не существует.")
        except Exception as e:
            st.error(f"Ошибка загрузки данных: {e}")


# import hashlib
#
#
# def get_hash(input_string, algorithm='sha256'):
#     """
#     Генерирует однозначный хэш для заданной строки.
#
#     :param input_string: Строка для хэширования.
#     :param algorithm: Алгоритм хэширования ('md5', 'sha1', 'sha256', 'sha512').
#     :return: Хэш-значение в виде шестнадцатеричной строки.
#     """
#     # Проверка на доступность алгоритма
#     if algorithm not in hashlib.algorithms_available:
#         raise ValueError(f"Алгоритм {algorithm} не поддерживается.")
#
#     # Создаем объект хэша
#     hash_object = hashlib.new(algorithm)
#     # Обновляем хэш объект входными данными
#     hash_object.update(input_string.encode('utf-8'))
#     # Возвращаем шестнадцатеричный хэш
#     return hash_object.hexdigest()
#
#
# # Пример использования
# input_data = "1"
# print("SHA-256 хэш:", get_hash(input_data, 'sha256'))
# print("MD5 хэш:", get_hash(input_data, 'md5'))


# 6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b