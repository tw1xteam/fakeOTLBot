# - *- coding: utf- 8 - *-
from typing import Union

from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.data.config import get_admins
from bot.database import Worker


class IsAdmin(BaseFilter):
    async def __call__(self, update: Union[Message, CallbackQuery], bot: Bot, state: FSMContext = None) -> bool:
        if not hasattr(update, "from_user") or update.from_user is None:
            return False

        if Worker.get(worker_id=update.from_user.id) is None:
            for admin in get_admins():
                if update.from_user.id == admin:
                    return True
            return False
        else:
            return True
