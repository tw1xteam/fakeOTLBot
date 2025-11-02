# - *- coding: utf- 8 - *-
import sqlite3
import json

from pydantic import BaseModel

from bot.data.config import PATH_DATABASE
from bot.database.db_helper import dict_factory, update_format_where, update_format
from bot.utils.const_functions import get_unix, ded, generate_deal_id


# Модель таблицы
class DealsModel(BaseModel):
    increment: int  # Инкремент
    deal_id: str  # Айди сделки
    deal_amount: float  # Сумма сделки
    deal_currency: str  # Валюта сделки
    deal_description: str  # Описание сделки
    deal_status: str  # Статус сделки
    deal_address: str  # Адрес отправки суммы за сделку
    deal_member: int | None  # Айди покупателя сделки


# Работа с сделками
class Deals:
    storage_name = "storage_deals"

    # Добавление записи
    @staticmethod
    def add(
            deal_id: str,
            deal_amount: float,
            deal_currency: str,
            deal_description: str,
            deal_address: str
    ):
        deal_member = 0
        deal_status = "waiting"

        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory

            con.execute(
                ded(f"""
                    INSERT INTO {Deals.storage_name} (
                        deal_id,
                        deal_amount,
                        deal_currency,
                        deal_description,
                        deal_status,
                        deal_address,
                        deal_member
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """),
                [
                    deal_id,
                    str(deal_amount),
                    deal_currency,
                    deal_description,
                    deal_status,
                    deal_address,
                    deal_member
                ],
            )

    # Получение записи
    @staticmethod
    def get(**kwargs) -> DealsModel:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Deals.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()

            if response is not None:
                response = DealsModel(**response)

            return response

    # Получение записей
    @staticmethod
    def gets(**kwargs) -> list[DealsModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Deals.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchall()

            if len(response) >= 1:
                response = [DealsModel(**cache_object) for cache_object in response]

            return response

    # Получение всех записей
    @staticmethod
    def get_all() -> list[DealsModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Deals.storage_name}"

            response = con.execute(sql).fetchall()

            if len(response) >= 1:
                response = [DealsModel(**cache_object) for cache_object in response]

            return response

    # Редактирование записи
    @staticmethod
    def update(deal_id, **kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Deals.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)
            parameters.append(deal_id)

            con.execute(sql + "WHERE deal_id = ?", parameters)

    # Удаление записи
    @staticmethod
    def delete(**kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Deals.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            con.execute(sql, parameters)

    # Очистка всех записей
    @staticmethod
    def clear():
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Deals.storage_name}"

            con.execute(sql)
