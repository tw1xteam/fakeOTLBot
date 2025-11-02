# - *- coding: utf- 8 - *-
import sqlite3
import json

from pydantic import BaseModel

from bot.data.config import PATH_DATABASE
from bot.database.db_helper import dict_factory, update_format_where, update_format
from bot.utils.const_functions import get_unix, ded


# Модель таблицы
class WorkerModel(BaseModel):
    increment: int  # Инкремент
    worker_id: int  # Айди воркера
    worker_deals_sucessful: int  # Количество успешно завершенных сделок
    worker_deals_cancel: int  # Количество закрытых сделок
    worker_prefix: str  # Префикс воркера
    worker_set_unix: int  # Дата добавления воркера


# Работа с юзером
class Worker:
    storage_name = "storage_workers"

    # Добавление записи
    @staticmethod
    def add(
            worker_id: int,
            worker_prefix: str
    ):
        worker_deals_sucessful = 0
        worker_deals_cancel = 0
        worker_set_unix = get_unix()

        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory

            con.execute(
                ded(f"""
                    INSERT INTO {Worker.storage_name} (
                        worker_id,
                        worker_deals_sucessful,
                        worker_deals_cancel,
                        worker_prefix,
                        worker_set_unix
                    ) VALUES (?, ?, ?, ?, ?)
                """),
                [
                    worker_id,
                    worker_deals_sucessful,
                    worker_deals_cancel,
                    worker_prefix,
                    worker_set_unix
                ],
            )

    # Получение записи
    @staticmethod
    def get(**kwargs) -> WorkerModel:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Worker.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchone()

            if response is not None:
                response = WorkerModel(**response)

            return response

    # Получение записей
    @staticmethod
    def gets(**kwargs) -> list[WorkerModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Worker.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            response = con.execute(sql, parameters).fetchall()

            if len(response) >= 1:
                response = [WorkerModel(**cache_object) for cache_object in response]

            return response

    # Получение всех записей
    @staticmethod
    def get_all() -> list[WorkerModel]:
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"SELECT * FROM {Worker.storage_name}"

            response = con.execute(sql).fetchall()

            if len(response) >= 1:
                response = [WorkerModel(**cache_object) for cache_object in response]

            return response

    # Редактирование записи
    @staticmethod
    def update(worker_id, **kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"UPDATE {Worker.storage_name} SET"
            sql, parameters = update_format(sql, kwargs)
            parameters.append(worker_id)

            con.execute(sql + "WHERE worker_id = ?", parameters)

    # Удаление записи
    @staticmethod
    def delete(**kwargs):
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Worker.storage_name}"
            sql, parameters = update_format_where(sql, kwargs)

            con.execute(sql, parameters)

    # Очистка всех записей
    @staticmethod
    def clear():
        with sqlite3.connect(PATH_DATABASE) as con:
            con.row_factory = dict_factory
            sql = f"DELETE FROM {Worker.storage_name}"

            con.execute(sql)
