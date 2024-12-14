import streamlit as st
import pandas as pd

def render(db, auth):
    """Страница загрузки данных из CSV."""
    # Проверяем доступ пользователя к загрузке данных в указанную таблицу
    user_id = st.session_state.user["user_id"]
    if not auth.has_permission(user_id, "upload_csv"):
        st.error("У вас нет прав для загрузки данных в эту таблицу.")
        return
    st.subheader("Загрузка данных из CSV")

    # Запрашиваем имя таблицы
    table_name = st.text_input("Введите имя таблицы для загрузки данных")
    uploaded_file = st.file_uploader("Выберите CSV-файл", type=["csv"])

    if uploaded_file and table_name:
        try:

            # Считываем CSV в DataFrame
            df = pd.read_csv(uploaded_file)
            st.write("Предпросмотр данных:")
            st.dataframe(df)

            if st.button("Загрузить данные в таблицу"):
                # Загружаем данные из DataFrame в таблицу
                db.insert_from_csv(table_name, df)
                st.success(f"Данные успешно загружены в таблицу `{table_name}`.")
        except Exception as e:
            st.error(f"Ошибка при загрузке данных: {e}")
