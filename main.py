# - *- coding: utf- 8 - *-
import asyncio
import os
import sys

import colorama
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from bot.data.config import get_admins, BOT_TOKEN, BOT_SCHEDULER
from bot.database.db_helper import create_dbx
from bot.middlewares import register_all_middlwares
from bot.routers import register_all_routers
from bot.services.api_session import AsyncRequestSession
from bot.utils.misc.bot_commands import set_commands
from bot.utils.misc.bot_logging import bot_logger

colorama.init()


async def main():
    BOT_SCHEDULER.start()
    dp = Dispatcher()
    arSession = AsyncRequestSession()
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
    )

    i18n = I18nMiddleware(
        core=FluentRuntimeCore(
            path="bot/assets/locales/{locale}"
        ),
        default_locale="ru"
    )
    i18n.setup(dp)

    register_all_middlwares(dp)  # Регистрация всех мидлварей
    register_all_routers(dp)  # Регистрация всех роутеров

    try:
        await set_commands(bot)

        bot_logger.warning("BOT WAS STARTED")
        print(colorama.Fore.LIGHTYELLOW_EX + f"~~~~~ Bot was started - @{(await bot.get_me()).username} ~~~~~")
        print(colorama.Fore.LIGHTBLUE_EX + "~~~~~ TG developer - @gde_tw1ks ~~~~~")
        print(colorama.Fore.RESET)

        if len(get_admins()) == 0:
            print("***** ENTER ADMIN ID IN settings.ini *****")

        await bot.delete_webhook()
        await bot.get_updates(offset=-1)

        await dp.start_polling(
            bot,
            arSession=arSession,
            allowed_updates=dp.resolve_used_update_types(),
        )
    finally:
        await arSession.close()
        await bot.session.close()


if __name__ == "__main__":
    create_dbx()  # Создание таблиц в базе данных

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        bot_logger.warning("Bot was stopped")
    finally:
        if sys.platform.startswith("win"):
            os.system("cls")
        else:
            os.system("clear")