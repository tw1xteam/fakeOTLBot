# - *- coding: utf- 8 - *-
from aiogram import Dispatcher, F

from bot.routers import main_errors, main_start, main_missed
from bot.routers.user import user_menu, user_deals
from bot.routers.admin import admin_menu
from bot.utils.misc.bot_filters import IsAdmin


# Регистрация всех роутеров
def register_all_routers(dp: Dispatcher):
    # Подключение фильтров
    dp.message.filter(F.chat.type == "private")  # Работа бота только в личке - сообщения
    dp.callback_query.filter(F.message.chat.type == "private")  # Работа бота только в личке - колбэки

    admin_menu.router.message.filter(IsAdmin())

    # Подключение обязательных роутеров
    dp.include_router(main_errors.router)  # Роутер ошибки
    dp.include_router(main_start.router)  # Роутер основных команд

    # Подключение пользовательских роутеров (юзеров и админов)
    dp.include_router(user_menu.router)
    dp.include_router(admin_menu.router)
    dp.include_router(user_deals.router)

    # Подключение обязательных роутеров
    dp.include_router(main_missed.router)  # Роутер пропущенных апдейтов