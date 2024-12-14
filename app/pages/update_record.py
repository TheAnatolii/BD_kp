import streamlit as st


def render(db, auth):
    """Страница обновления записи."""
    # Проверяем доступ пользователя к обновлению записей в этой таблице
    user_id = st.session_state.user["user_id"]
    if not auth.has_permission(user_id, "update_record"):
        st.error("У вас нет прав для обновления записей в этой таблице.")
        return
    st.subheader("Обновление записи")

    # Запрашиваем имя таблицы
    table_name = st.text_input("Введите имя таблицы")

    if table_name:
        try:

            # Получаем колонки таблицы
            columns = db.get_columns(table_name)
            unique_identifier = db.get_unique_identifier(table_name)

            if columns and unique_identifier:
                # Запрашиваем уникальный идентификатор записи
                unique_id_value = st.text_input(
                    f"Введите значение для уникального идентификатора `{unique_identifier}`")

                # Генерируем поля ввода для обновления данных
                input_data = {
                    col: st.text_input(f"Новое значение для {col} (оставьте пустым для пропуска)") for col in columns
                }

                if st.button("Обновить запись"):
                    # Убираем пустые значения из обновляемых данных
                    filtered_data = {k: v for k, v in input_data.items() if v}

                    if filtered_data:
                        # Обновляем запись в базе данных
                        db.update_record(table_name, unique_id_value, filtered_data)
                        st.success("Запись успешно обновлена!")
                    else:
                        st.warning("Нет данных для обновления.")
            else:
                st.warning("Не удалось получить информацию о таблице. Убедитесь, что таблица существует.")
        except Exception as e:
            st.error(f"Ошибка при обновлении записи: {e}")
