# - *- coding: utf- 8 - *-
import configparser

from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_CONFIG = configparser.ConfigParser()
BOT_CONFIG.read("settings.ini")

# Образы и конфиги
BOT_TOKEN = BOT_CONFIG['settings']['bot_token'].strip().replace(' ', '')  # Токен бота
GROUP_ID = BOT_CONFIG['settings']['group_id']  # ID группы для отправки лог-сообщений.
TOPIC_ID = BOT_CONFIG['settings']['topic_reply_id']  # ID сообщения создания топика для отправки сообщений в конкретный топик.
BOT_TIMEZONE = "Europe/Moscow"  # Временная зона бота
BOT_SCHEDULER = AsyncIOScheduler(timezone=BOT_TIMEZONE)  # Образ шедулера
BOT_VERSION = 1.0  # Версия бота

# Пути к файлам
PATH_DATABASE = "bot/data/database.db"  # Путь к Базе Данных
PATH_LOGS = "bot/data/logs.log"  # Путь к Логам


# Получение администраторов бота
def get_admins() -> list[int]:
    read_admins = configparser.ConfigParser()
    read_admins.read("settings.ini")

    admins = read_admins['settings']['admin_id'].strip().replace(" ", "")

    if "," in admins:
        admins = admins.split(",")
    else:
        if len(admins) >= 1:
            admins = [admins]
        else:
            admins = []

    while "" in admins: admins.remove("")
    while " " in admins: admins.remove(" ")
    while "\r" in admins: admins.remove("\r")
    while "\n" in admins: admins.remove("\n")

    admins = list(map(int, admins))

    return admins


def get_desc():
    return """
        Бот создан @gde_tw1ks.
        На базе djimbo.
        Функционал сделан: @gde_tw1ks (tg, id: 8032099011).
        Идея: @iquse_scm (tg, id: 5828344752)
    """
