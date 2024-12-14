import yaml
import hashlib
import os
from dotenv import load_dotenv


def load_env_variables(env_file_path="/Users/anatolii/Универ/BD/КП/config/env.env"):
    """
    Extracts database configuration from a .env file.
    :param env_file_path: Path to the .env file.
    :return: Dictionary containing the database configuration.
    """
    load_dotenv(f"{env_file_path}")
    # Чтение и установка env
    DB_CONFIG = {
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "min_pool": int(os.getenv("POOL_MIN_CONN", 1)),
        "max_pool": int(os.getenv("POOL_MAX_CONN", 10))
    }
    return DB_CONFIG

def load_unique_identifiers(config_path):
    """
        Загружает имена уникальных идентификаторов для таблиц из YAML-файла.
        """
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
            return config.get("unique_identifiers", {})
    except Exception as e:
        print(f"Ошибка загрузки конфигурации уникальных идентификаторов: {e}")
        return {}

def quote_identifier(identifier):
    """Добавляет кавычки к имени таблицы или столбца."""
    if not identifier.startswith('"') and not identifier.endswith('"'):
        return f'"{identifier}"'
    return identifier

def get_hash(input_string, algorithm='sha256'):
    """
    Генерирует однозначный хэш для заданной строки.

    :param input_string: Строка для хэширования.
    :param algorithm: Алгоритм хэширования ('md5', 'sha1', 'sha256', 'sha512').
    :return: Хэш-значение в виде шестнадцатеричной строки.
    """
    # Проверка на доступность алгоритма
    if algorithm not in hashlib.algorithms_available:
        raise ValueError(f"Алгоритм {algorithm} не поддерживается.")

    # Создаем объект хэша
    hash_object = hashlib.new(algorithm)
    # Обновляем хэш объект входными данными
    hash_object.update(input_string.encode('utf-8'))
    # Возвращаем шестнадцатеричный хэш
    return hash_object.hexdigest()