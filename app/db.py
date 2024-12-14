# import psycopg2
# from psycopg2.extras import RealDictCursor
# from app.utils import quote_identifier, load_unique_identifiers
#
# class Database:
#     def __init__(self, host, port, database, user, password, config_path='/Users/anatolii/Универ/BD/КП/config/unique_identifiers.yaml'):
#         self.connection = psycopg2.connect(
#             host=host,
#             port=port,
#             dbname=database,
#             user=user,
#             password=password,
#             async_=True
#         )
#         self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
#         self.unique_identifiers = load_unique_identifiers(config_path)
#
#     def get_unique_identifier(self, table_name):
#         """
#         Возвращает имя уникального идентификатора таблицы из конфигурации.
#         """
#         return self.unique_identifiers.get(table_name)
#
#     def fetch_one(self, query, params=None):
#         """
#         Выполняет SQL-запрос и возвращает одну запись.
#         :param query: SQL-запрос.
#         :param params: Параметры для подстановки в запрос.
#         :return: Словарь с данными одной записи.
#         """
#         try:
#             self.cursor.execute(query, params or ())
#             return self.cursor.fetchone()
#         except Exception as e:
#             print(f"Ошибка выполнения запроса: {e}")
#             return None
#
#     def get_columns(self, table_name):
#         try:
#             table_name = quote_identifier(table_name)
#             self.cursor.execute(f"""
#                 SELECT column_name
#                 FROM information_schema.columns
#                 WHERE table_name = %s
#             """, (table_name.strip('"'),))  # Таблицы в information_schema всегда в нижнем регистре
#             return [row['column_name'] for row in self.cursor.fetchall()]
#         except Exception as e:
#             print(f"Ошибка получения колонок: {e}")
#             return None
#
#     def insert_record(self, table_name, data):
#         try:
#             table_name = quote_identifier(table_name)
#             columns = ", ".join([quote_identifier(col) for col in data.keys()])
#             values_placeholder = ", ".join(["%s"] * len(data))
#             self.cursor.execute(
#                 f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder})",
#                 list(data.values())
#             )
#             self.connection.commit()
#         except Exception as e:
#             print(f"Ошибка добавления записи: {e}")
#
#     def update_record(self, table_name, record_id, data):
#         """Обновляет запись, используя первый столбец как идентификатор."""
#         try:
#             id_column = self.get_unique_identifier(table_name)
#             if not id_column:
#                 raise ValueError("Не удалось определить идентификатор таблицы.")
#             table_name = quote_identifier(table_name)
#             id_column = quote_identifier(id_column)
#             updates = ", ".join([f"{quote_identifier(key)} = %s" for key in data.keys()])
#             values = list(data.values()) + [record_id]
#             self.cursor.execute(
#                 f"UPDATE {table_name} SET {updates} WHERE {id_column} = %s",
#                 values
#             )
#             self.connection.commit()
#         except Exception as e:
#             print(f"Ошибка обновления записи: {e}")
#
#     def delete_record(self, table_name, record_id):
#         """Удаляет запись, используя первый столбец как идентификатор."""
#         try:
#             id_column = self.get_unique_identifier(table_name)
#             if not id_column:
#                 raise ValueError("Не удалось определить идентификатор таблицы.")
#             table_name = quote_identifier(table_name)
#             id_column = quote_identifier(id_column)
#             self.cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = %s", (record_id,))
#             self.connection.commit()
#         except Exception as e:
#             print(f"Ошибка удаления записи: {e}")
#
#     def insert_from_csv(self, table_name, dataframe):
#         try:
#             # Получаем первичный ключ для таблицы
#             primary_key = self.get_unique_identifier(table_name)
#
#             table_name = quote_identifier(table_name)
#             columns = [quote_identifier(col) for col in dataframe.columns]
#             columns_joined = ", ".join(columns)
#             values_placeholder = ", ".join(["%s"] * len(columns))
#
#             if not primary_key:
#                 raise ValueError("Не удалось определить первичный ключ таблицы.")
#
#             # Генерируем часть запроса для обновления в случае конфликта
#             update_clause = ", ".join(
#                 [f"{col} = EXCLUDED.{col}" for col in columns if col != quote_identifier(primary_key)]
#             )
#
#             # Запрос с использованием INSERT ... ON CONFLICT
#             query = f"""
#             INSERT INTO {table_name} ({columns_joined})
#             VALUES ({values_placeholder})
#             ON CONFLICT ({quote_identifier(primary_key)})
#             DO UPDATE SET {update_clause};
#             """
#
#             # Преобразуем строки DataFrame в кортежи
#             values = [tuple(row) for row in dataframe.to_numpy()]
#
#             # Выполняем запрос для каждой строки
#             self.cursor.executemany(query, values)
#             self.connection.commit()
#             print(f"Данные из CSV успешно загружены или обновлены в таблице {table_name}.")
#         except Exception as e:
#             print(f"Ошибка загрузки данных из CSV: {e}")
#
#     def get_table_relationships(self, table_name):
#         """
#         Возвращает список внешних ключей (связей) для указанной таблицы.
#         """
#         try:
#             query = """
#             SELECT
#                 kcu.column_name AS local_column,
#                 ccu.table_name AS referenced_table,
#                 ccu.column_name AS referenced_column
#             FROM
#                 information_schema.table_constraints AS tc
#                 JOIN information_schema.key_column_usage AS kcu
#                 ON tc.constraint_name = kcu.constraint_name
#                 AND tc.table_schema = kcu.table_schema
#                 JOIN information_schema.constraint_column_usage AS ccu
#                 ON ccu.constraint_name = tc.constraint_name
#                 AND ccu.table_schema = tc.table_schema
#             WHERE
#                 tc.constraint_type = 'FOREIGN KEY'
#                 AND tc.table_name = %s;
#             """
#             self.cursor.execute(query, (table_name,))
#             return self.cursor.fetchall()
#         except Exception as e:
#             print(f"Ошибка получения связей таблицы {table_name}: {e}")
#
#     def fetch_joined_data(self, table_name, limit=100, offset=0):
#         """
#         Выбирает данные из таблицы вместе с данными из связанных таблиц в виде объединенных колонок.
#         """
#         try:
#             relationships = self.get_table_relationships(table_name)
#             main_table = quote_identifier(table_name)
#
#             if not relationships:
#                 self.cursor.execute(
#                     f"SELECT * FROM {main_table} LIMIT %s OFFSET %s", (limit, offset)
#                 )
#                 return self.cursor.fetchall()
#
#             select_clause = [f"{main_table}.*"]
#             join_clause = ""
#             added_columns = set()
#
#             for rel in relationships:
#                 related_table = quote_identifier(rel['referenced_table'])
#                 local_column = quote_identifier(rel['local_column'])
#                 referenced_column = quote_identifier(rel['referenced_column'])
#
#                 related_columns = self.get_columns(rel['referenced_table'])
#                 if not related_columns:
#                     continue
#
#                 for col in related_columns:
#                     alias = f"{rel['referenced_table']}_{col}"
#                     if alias not in added_columns and col != rel['referenced_column']:
#                         select_clause.append(f"{related_table}.{quote_identifier(col)} AS {quote_identifier(alias)}")
#                         added_columns.add(alias)
#
#                 join_clause += f"""
#                 LEFT JOIN {related_table}
#                 ON {main_table}.{local_column} = {related_table}.{referenced_column}
#                 """
#
#             query = f"""
#             SELECT {', '.join(select_clause)}
#             FROM {main_table}
#             {join_clause}
#             LIMIT %s OFFSET %s
#             """
#             self.cursor.execute(query, (limit, offset))
#             return self.cursor.fetchall()
#
#         except Exception as e:
#             print(f"Ошибка загрузки данных с объединением для таблицы {table_name}: {e}")
#             return None
#
# def __del__(self):
#     self.cursor.close()
#     self.connection.close()


import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from app.utils import quote_identifier, load_unique_identifiers
from psycopg2.errors import UniqueViolation


class Database:

    def __init__(self, database, host, port, user, password,
                 config_path='/Users/anatolii/Универ/BD/КП/config/unique_identifiers.yaml',
                 min_pool=1, max_pool=10):
        self.pool = psycopg2.pool.SimpleConnectionPool(
            min_pool,
            max_pool,
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password
        )
        # self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        self.unique_identifiers = load_unique_identifiers(config_path)


    def get_connection(self):
        """
        Получает соединение из пула.
        """
        return self.pool.getconn()

    def release_connection(self, conn):
        """
        Освобождает соединение, возвращая его в пул.
        """
        self.pool.putconn(conn)

    def get_unique_identifier(self, table_name):
        """
        Возвращает имя уникального идентификатора таблицы из конфигурации.
        """
        return self.unique_identifiers.get(table_name)

    def fetch_one(self, query, params=None):
        """
        Выполняет SQL-запрос и возвращает одну запись.
        :param query: SQL-запрос.
        :param params: Параметры для подстановки в запрос.
        :return: Словарь с данными одной записи.
        """
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchone()
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return None
        finally:
            self.release_connection(conn)

    def get_columns(self, table_name):
        conn = self.get_connection()
        try:
            table_name = quote_identifier(table_name)
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = %s
                """, (table_name.strip('"'),))
                return [row['column_name'] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Ошибка получения колонок: {e}")
            return None
        finally:
            self.release_connection(conn)

    def insert_record(self, table_name, data):
        conn = self.get_connection()
        try:
            table_name = quote_identifier(table_name)
            columns = ", ".join([quote_identifier(col) for col in data.keys()])
            values_placeholder = ", ".join(["%s"] * len(data))
            with conn.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder})",
                    list(data.values())
                )
                conn.commit()
        except UniqueViolation:
            conn.rollback()  # Откатить изменения в случае ошибки
            raise UniqueViolation("Duplicate key value violates unique constraint")
        except Exception as e:
            print(f"Ошибка добавления записи: {e}")
        finally:
            self.release_connection(conn)

    def update_record(self, table_name, record_id, data):
        """Обновляет запись, используя первый столбец как идентификатор."""
        conn = self.get_connection()
        try:
            id_column = self.get_unique_identifier(table_name)
            if not id_column:
                raise ValueError("Не удалось определить идентификатор таблицы.")
            table_name = quote_identifier(table_name)
            id_column = quote_identifier(id_column)
            updates = ", ".join([f"{quote_identifier(key)} = %s" for key in data.keys()])
            values = list(data.values()) + [record_id]
            with conn.cursor() as cursor:
                cursor.execute(
                    f"UPDATE {table_name} SET {updates} WHERE {id_column} = %s",
                    values
                )
                conn.commit()
        except Exception as e:
            print(f"Ошибка обновления записи: {e}")
        finally:
            self.release_connection(conn)

    def delete_record(self, table_name, record_id):
        """Удаляет запись, используя первый столбец как идентификатор."""
        conn = self.get_connection()
        try:
            id_column = self.get_unique_identifier(table_name)
            if not id_column:
                raise ValueError("Не удалось определить идентификатор таблицы.")
            table_name = quote_identifier(table_name)
            id_column = quote_identifier(id_column)
            with conn.cursor() as cursor:
                cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = %s", (record_id,))
                conn.commit()
        except Exception as e:
            print(f"Ошибка удаления записи: {e}")
        finally:
            self.release_connection(conn)

    def insert_from_csv(self, table_name, dataframe):
        conn = self.get_connection()
        try:
            primary_key = self.get_unique_identifier(table_name)

            table_name = quote_identifier(table_name)
            columns = [quote_identifier(col) for col in dataframe.columns]
            columns_joined = ", ".join(columns)
            values_placeholder = ", ".join(["%s"] * len(columns))

            if not primary_key:
                raise ValueError("Не удалось определить первичный ключ таблицы.")

            update_clause = ", ".join(
                [f"{col} = EXCLUDED.{col}" for col in columns if col != quote_identifier(primary_key)]
            )

            query = f"""
            INSERT INTO {table_name} ({columns_joined})
            VALUES ({values_placeholder})
            ON CONFLICT ({quote_identifier(primary_key)}) 
            DO UPDATE SET {update_clause};
            """

            values = [tuple(row) for row in dataframe.to_numpy()]

            with conn.cursor() as cursor:
                cursor.executemany(query, values)
                conn.commit()
            print(f"Данные из CSV успешно загружены или обновлены в таблице {table_name}.")
        except Exception as e:
            print(f"Ошибка загрузки данных из CSV: {e}")
        finally:
            self.release_connection(conn)

    def get_table_relationships(self, table_name):
        conn = self.get_connection()
        try:
            query = """
            SELECT
                kcu.column_name AS local_column,
                ccu.table_name AS referenced_table,
                ccu.column_name AS referenced_column
            FROM
                information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            WHERE
                tc.constraint_type = 'FOREIGN KEY'
                AND tc.table_name = %s;
            """
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (table_name,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка получения связей таблицы {table_name}: {e}")
            return None
        finally:
            self.release_connection(conn)

    def fetch_joined_data(self, table_name, limit=100, offset=0):
        """
        Выбирает данные из таблицы вместе с данными из связанных таблиц в виде объединенных колонок.
        """
        conn = self.get_connection()
        try:
            relationships = self.get_table_relationships(table_name)
            main_table = quote_identifier(table_name)

            if not relationships:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(
                        f"SELECT * FROM {main_table} LIMIT %s OFFSET %s", (limit, offset)
                    )
                    return cursor.fetchall()

            select_clause = [f"{main_table}.*"]
            join_clause = ""
            added_columns = set()

            for rel in relationships:
                related_table = quote_identifier(rel['referenced_table'])
                local_column = quote_identifier(rel['local_column'])
                referenced_column = quote_identifier(rel['referenced_column'])

                related_columns = self.get_columns(rel['referenced_table'])
                if not related_columns:
                    continue

                for col in related_columns:
                    alias = f"{rel['referenced_table']}_{col}"
                    if alias not in added_columns and col != rel['referenced_column']:
                        select_clause.append(f"{related_table}.{quote_identifier(col)} AS {quote_identifier(alias)}")
                        added_columns.add(alias)

                join_clause += f"""
                LEFT JOIN {related_table}
                ON {main_table}.{local_column} = {related_table}.{referenced_column}
                """

            query = f"""
            SELECT {', '.join(select_clause)}
            FROM {main_table}
            {join_clause}
            LIMIT %s OFFSET %s
            """
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, (limit, offset))
                return cursor.fetchall()

        except Exception as e:
            print(f"Ошибка загрузки данных с объединением для таблицы {table_name}: {e}")
            return None
        finally:
            self.release_connection(conn)

    def __del__(self):
        if self.pool:
            self.pool.closeall()

