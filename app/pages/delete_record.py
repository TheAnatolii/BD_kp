import streamlit as st


def render(db, auth):
    """Страница удаления записи."""
    # Проверяем доступ пользователя к удалению записей в этой таблице
    user_id = st.session_state.user["user_id"]
    if not auth.has_permission(user_id, "delete_record"):
        st.error("У вас нет прав для удаления записей из этой таблицы.")
        return
    st.subheader("Удаление записи")

    # Запрашиваем имя таблицы
    table_name = st.text_input("Введите имя таблицы")

    if table_name:
        try:

            # Запрашиваем ID записи
            record_id = st.number_input("Введите ID записи для удаления", min_value=1, step=1)

            if st.button("Удалить запись"):
                # Удаляем запись из базы данных
                db.delete_record(table_name, record_id)
                st.success(f"Запись с ID {record_id} успешно удалена из таблицы `{table_name}`.")
        except Exception as e:
            st.error(f"Ошибка при удалении записи: {e}")
