# - *- coding: utf- 8 - *-
from aiogram import Dispatcher

from bot.middlewares.middleware_users import ExistsUserMiddleware


# Регистрация всех миддлварей
def register_all_middlwares(dp: Dispatcher):
    dp.callback_query.outer_middleware(ExistsUserMiddleware())
    dp.message.outer_middleware(ExistsUserMiddleware())