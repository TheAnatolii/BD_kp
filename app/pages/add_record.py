import streamlit as st
from app.utils import get_hash
from psycopg2.errors import UniqueViolation

def render(db, auth):
    """Страница добавления записи."""
    # Проверяем доступ пользователя к добавлению записей в эту таблицу
    user_id = st.session_state.user["user_id"]
    if not auth.has_permission(user_id, "add_record"):
        st.error("У вас нет прав для добавления записи в эту таблицу.")
        return
    st.subheader("Добавление записи")

    # Запрашиваем имя таблицы
    table_name = st.text_input("Введите имя таблицы")

    if table_name:
        try:

            # Получаем колонки таблицы
            columns = db.get_columns(table_name)
            if columns:
                # Генерируем поля ввода для каждой колонки
                input_data = {col: st.text_input(f"Введите значение для {col}") for col in columns}
                print(input_data)
                if table_name == "Users":
                    # if 'hash_password' in input_data and input_data['hash_password']:
                    input_data["hash_password"] = get_hash(input_data['hash_password'])

                if st.button("Добавить запись"):
                    try:
                        # Добавляем запись в базу данных
                        db.insert_record(table_name, input_data)
                        st.success("Запись успешно добавлена!")
                    except UniqueViolation:
                        st.error("Ошибка: запись с таким id уже существует.")
                    except Exception as e:
                        st.error(f"Ошибка при добавлении записи: {e}")
            else:
                st.warning("Не удалось получить колонки таблицы. Убедитесь, что таблица существует.")
        except Exception as e:
            st.error(f"Ошибка при добавлении записи: {e}")
