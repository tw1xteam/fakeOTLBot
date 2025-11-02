# - *- coding: utf- 8 - *-
import sqlite3
import json

from pydantic import BaseModel

from bot.data.config import PATH_DATABASE
from bot.database.db_helper import dict_factory, update_format_where, update_format
from bot.utils.const_functions import get_unix, ded


# Модель таблицы
class ReferralModel(BaseModel):
    increment: int  # Инкремент
    refferal_id: int   # Айди приглашенного реферала
    refferal_owner: int  # Айди владельца реферала


# Работа с юзером
class Referrals:
    storage_name = "storage_referrals"

    # Добавление записи
    @staticmethod
    def add(
            refferal_id: int,
            refferal_owner: int
    ):
        refferal_purchase = 0
        refferal_unix = get_unix()

        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory

            con.execute(
                ded(f"""
                    INSERT INTO {Referrals.storage_name} (
                        refferal_id,
                        refferal_owner,
                        refferal_purchase,
                        refferal_unix
                    ) VALUES (?, ?, ?, ?)
                """),
                [
                    refferal_id,
                    refferal_owner,
                    refferal_purchase,
                    refferal_unix
                ],
            )

    # Получение записи
    @staticmethod
    def get(**kwargs) -> ReferralModel:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Referrals.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()

            if response is not None:
                response = ReferralModel(**response)

            return response

    # Получение записей
    @staticmethod
    def gets(**kwargs) -> list[ReferralModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Referrals.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchall()

            if len(response) >= 1:
                response = [ReferralModel(**cache_object) for cache_object in response]

            return response

    # Получение всех записей
    @staticmethod
    def get_all() -> list[ReferralModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Referrals.storage_name}"

            response = con.execute(sql).fetchall()

            if len(response) >= 1:
                response = [ReferralModel(**cache_object) for cache_object in response]

            return response

    # Редактирование записи
    @staticmethod
    def update(user_id, **kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Referrals.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)
            parameters.append(user_id)

            con.execute(sql + "WHERE refferal_id = ?", parameters)

    # Удаление записи
    @staticmethod
    def delete(**kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Referrals.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            con.execute(sql, parameters)

    # Очистка всех записей
    @staticmethod
    def clear():
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Referrals.storage_name}"

            con.execute(sql)
