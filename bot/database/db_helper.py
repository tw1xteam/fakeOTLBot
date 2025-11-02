# - *- coding: utf- 8 - *-
import sqlite3

from bot.data.config import PATH_DATABASE
from bot.utils.const_functions import get_unix, ded


# Преобразование полученного списка в словарь
def dict_factory(cursor, row) -> dict:
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict


# Форматирование запроса без аргументов
def update_format(sql, parameters: dict) -> tuple[str, list]:
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql += f" {values}"

    return sql, list(parameters.values())


# Форматирование запроса с аргументами
def update_format_where(sql, parameters: dict) -> tuple[str, list]:
    sql += " WHERE "

    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])

    return sql, list(parameters.values())


################################################################################
# Создание всех таблиц для БД
def create_dbx():
    with sqlite3.connect(PATH_DATABASE) as con:
        con.row_factory = dict_factory

        ############################################################
        # Создание таблицы с хранением - Пользователей
        if len(con.execute("PRAGMA table_info(storage_users)").fetchall()) == 9:
            print("TABLE `users` was found(1/4)")
        else:
            con.execute(
                ded(f"""
                    CREATE TABLE storage_users(
                        increment INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        user_login TEXT,
                        user_name TEXT,
                        refferal_count INTEGER DEFAULT 0,
                        sucessful_deals INTEGER DEFAULT 0,
                        user_ton_wallet TEXT,
                        user_card_wallet TEXT,
                        user_unix INTEGER
                    )
                """)
            )
            print("TABLE `users` was not found(1/4) | Creating...")

        # Создание таблицы с хранением - Рефераллов
        if len(con.execute("PRAGMA table_info(storage_referrals)").fetchall()) == 5:
            print("TABLE `referrals` was found(2/4)")
        else:
            con.execute(
                ded(f"""
                    CREATE TABLE storage_referrals(
                        increment INTEGER PRIMARY KEY AUTOINCREMENT,
                        refferal_id INTEGER,
                        refferal_owner INTEGER,
                        refferal_purchase INTEGER DEFAULT 0,
                        refferal_unix INTEGER
                    )
                """)
            )
            print("TABLE `referrals` was not found(2/4) | Creating...")

        # Создание таблицы с хранением - Сделок
        if len(con.execute("PRAGMA table_info(storage_deals)").fetchall()) == 8:
            print("TABLE `deals` was found(3/4)")
        else:
            con.execute(
                ded(f"""
                    CREATE TABLE storage_deals(
                        increment INTEGER PRIMARY KEY AUTOINCREMENT,
                        deal_id TEXT UNIQUE NOT NULL ,
                        deal_amount REAL NOT NULL,
                        deal_currency TEXT NOT NULL DEFAULT "TON",
                        deal_description TEXT NOT NULL,
                        deal_status TEXT NOT NULL DEFAULT "waiting",
                        deal_address TEXT NOT NULL,
                        deal_member INTEGER NOT NULL
                    )
                """)
            )
            print("TABLE `deals` was not found(3/4) | Creating...")

        # Создание таблицы с хранением - Сделок
        if len(con.execute("PRAGMA table_info(storage_workers)").fetchall()) == 6:
            print("TABLE `admins` was found(4/4)")
        else:
            con.execute(
                ded(f"""
                    CREATE TABLE storage_workers(
                        increment INTEGER PRIMARY KEY AUTOINCREMENT,
                        worker_id INTEGER NOT NULL,
                        worker_deals_sucessful INTEGER DEFAULT 0,
                        worker_deals_cancel INTEGER DEFAULT 0,
                        worker_prefix TEXT NOT NULL,
                        worker_set_unix INTEGER DEFAULT 0
                    )
                """)
            )
            print("TABLE `admins` was not found(4/4) | Creating...")