# - *- coding: utf- 8 - *-
from typing import Union

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from bot.data.config import get_admins
from bot.database import Worker, Userx, Deals, WorkerModel
from bot.utils.const_functions import ikb, format_float_to_12_digits


################################################################################
#################################### ПРОЧЕЕ ####################################
# Открытие главного меню
def main_admin(owner: bool = False) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Управление сделками", "admin_deals")
    )

    keyboard.row(
        ikb("⚙️ Накрут статистики", "add_stats")
    )

    if owner:
        keyboard.row(
            ikb("👥️ Управление администраторами", "manage_admins")
        )

    return keyboard.as_markup()


# Открытие сделок
def select_deals(worker: WorkerModel, is_admin: bool) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    filtered_deals = [
        deal for deal in Deals.get_all()
        if (worker is None and is_admin) or
           deal.deal_member == 0 or
           (worker is not None and deal.deal_member == worker.worker_id)
    ]

    for deal in filtered_deals:
        keyboard.row(
            ikb(f"💼 Сделка {deal.deal_id} ({deal.deal_amount} {deal.deal_currency.upper()})",
                f"edit_deal:{deal.deal_id}")
        )

    keyboard.row(
        ikb("🔙 Вернуться в меню", "back_admin")
    )

    return keyboard.as_markup()


def edit_deal(deal_id: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✅ Подтвердить оплату", f"confirm_deal:{deal_id}")
    )

    keyboard.row(
        ikb("❌ Отменить сделку", f"cancel_deal:{deal_id}")
    )

    keyboard.row(
        ikb("🔙 Вернуться в меню", "back_admin")
    )

    return keyboard.as_markup()


# Выбор что именно делать
def admin_edits() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("📋 Список воркеров", "admin_list"),
        ikb("➕ Добавить воркера", "admin_add")
    )

    keyboard.row(
        ikb("🔙 Вернуться в меню", "back_admin")
    )
    return keyboard.as_markup()


# Возврат в главное меню
def admin_back() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("🔙 Вернуться в меню", "back_admin")
    )

    return keyboard.as_markup()


def admin_markup_list(page: int = 0, per_page: int = 8) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    all_workers = Worker.get_all()
    total_workers = len(all_workers)
    total_pages = max(1, (total_workers + per_page - 1) // per_page)

    page_workers = all_workers[page * per_page: (page + 1) * per_page]

    for worker in page_workers:
        worker_user = Userx.get(user_id=worker.worker_id)
        if worker_user:
            builder.row(
                ikb(
                    f"👤 {worker_user.user_login} - {worker.worker_prefix}",
                    data=f"select_worker:{worker.worker_id}"
                )
            )

    pagination_buttons = []

    pagination_buttons.append(
        ikb(
            "⏪",
            data="admin_workers_page:0" if page != 0 else "..."
        )
    )

    if total_pages > 1:
        data_xyu = ""
        if page > 0:
            data_xyu = f"admin_workers_page:{page - 1}"
        else:
            data_xyu = f"..."
        pagination_buttons.append(
            ikb(
                "⬅️",
                data=data_xyu
            )
        )

        pagination_buttons.append(
            ikb(
                f"{page + 1}/{total_pages}",
                data="..."
            )
        )

        pagination_buttons.append(
            ikb(
                "➡️",
                data=f"admin_workers_page:{page + 1}" if page != total_pages - 1 else "..."
            )
        )



    if pagination_buttons:
        pagination_buttons.append(
            ikb(
                "⏩",
                data=f"admin_workers_page:{total_pages - 1}"
            )
        )
        builder.row(*pagination_buttons)

    builder.row(
        ikb(
            "🔙 Вернуться в меню",
            data="back_admin"
        )
    )

    return builder.as_markup()


# Редактирования воркера
def worker_edit(worker_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("❌ Удалить", f"worker_delete:{worker_id}"),

        ikb("🔙 Вернуться в меню", "back_admin")
    )

    return keyboard.as_markup()
