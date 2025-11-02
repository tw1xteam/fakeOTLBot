# - *- coding: utf- 8 - *-
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from bot.data.config import get_admins
from bot.database import Worker

# Команды для юзеров
user_commands = [
    BotCommand(command='start', description='Open menu'),
]

# Команды для админов
admin_commands = [
    BotCommand(command='start', description='Open menu'),
    BotCommand(command='admin_panelb', description='Open admin')
]


# Установка команд
async def set_commands(bot: Bot):
    await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())

    for admin in get_admins():
        try:
            await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin))
        except:
            ...

    for worker in Worker.get_all():
        try:
            await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=worker.worker_id))
        except:
            ...