# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message, ReactionTypeEmoji
from aiogram_i18n import I18nContext
from pyexpat.errors import messages

from bot.database import Userx, Deals, Worker
from bot.keyboard.inline_admin import main_admin, admin_edits, admin_back, admin_markup_list, worker_edit, select_deals, \
    edit_deal
from bot.keyboard.inline_user import select_wallet_method, back_menu, deal_markup, select_card_currency, deal_confirmed
from bot.utils.const_functions import generate_deal_id, is_float, ded, convert_date, convert_day, get_unix, \
    is_wallet_ton
from bot.utils.misc.bot_models import FSM, ARS

router = Router(name=__name__)


@router.message(F.text == "/admin_panelb")
async def admin_panelb(message: Message, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    await state.clear()

    worker = Worker.get(worker_id=message.from_user.id)

    if worker is None:
        admin_menu = await message.answer(
            ded(f"""
                🎉 <b>Вы перешли в админ-панель!</b>
                
                💎 <b>Ваша роль:</b> <code>Владелец</code>

                🔧 Здесь вы можете управлять сделками и участниками.
                👑 Добро пожаловать в эксклюзивный доступ!
                    """),
            reply_markup=main_admin(True)
        )
        await bot.set_message_reaction(chat_id=admin_menu.chat.id, message_id=admin_menu.message_id,
                                       reaction=[{"type": "emoji", "emoji": "👨‍💻"}])
        return

    admin_menu = await message.answer(
        ded(f"""
                    🎉 <b>Вы перешли в админ-панель!</b>
                    
                    💎 <b>Ваша роль:</b> <code>Воркер</code>
                    📌 <b>Ваш префикс:</b> <code>{worker.worker_prefix}</code>

                    🔧 Здесь вы можете управлять сделками и участниками.
                    👑 Добро пожаловать в эксклюзивный доступ!
                """),
        reply_markup=main_admin()
    )

    await bot.set_message_reaction(chat_id=admin_menu.chat.id, message_id=admin_menu.message_id,
                                   reaction=[{"type": "emoji", "emoji": "👨‍💻"}])


@router.callback_query(F.data == "back_admin")
async def back_admin(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    await state.clear()

    worker = Worker.get(worker_id=call.from_user.id)

    if worker is None:
        admin_menu = await call.message.edit_text(
            ded(f"""
                🎉 <b>Вы перешли в админ-панель!</b>

                💎 <b>Ваша роль:</b> <code>Владелец</code>

                🔧 Здесь вы можете управлять сделками и участниками.
                👑 Добро пожаловать в эксклюзивный доступ!
                    """),
            reply_markup=main_admin(True)
        )
        await bot.set_message_reaction(chat_id=admin_menu.chat.id, message_id=admin_menu.message_id,
                                       reaction=[{"type": "emoji", "emoji": "👨‍💻"}])
        return

    admin_menu = await call.message.edit_text(
        ded(f"""
                    🎉 <b>Вы перешли в админ-панель!</b>

                    💎 <b>Ваша роль:</b> <code>Воркер</code>
                    📌 <b>Ваш префикс:</b> <code>{worker.worker_prefix}</code>

                    🔧 Здесь вы можете управлять сделками и участниками.
                    👑 Добро пожаловать в эксклюзивный доступ!
                """),
        reply_markup=main_admin()
    )

    await bot.set_message_reaction(chat_id=admin_menu.chat.id, message_id=admin_menu.message_id,
                                   reaction=[{"type": "emoji", "emoji": "👨‍💻"}])


@router.callback_query(F.data == "manage_admins")
async def manage_admins(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    await state.clear()

    worker = Worker.get(worker_id=call.from_user.id)

    if worker is not None:
        return

    await call.message.edit_text(ded("""
        👥 <b>Управление администраторами</b>
        Выберите действие из меню ниже.
    """),
                                 reply_markup=admin_edits())


@router.callback_query(F.data == "admin_add")
async def admin_add(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    await state.clear()

    worker = Worker.get(worker_id=call.from_user.id)

    if worker is not None:
        return

    await call.message.edit_text(ded("""
        ➕ <b>Добавление воркера.</b>
        
        Введите username пользователя для добавления в формате: <code>@example_username</code>
    """), reply_markup=admin_back())
    await state.set_state("admin_add_name")


@router.message(F.text, StateFilter("admin_add_name"))
async def admin_add_name(message: Message, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    username = message.text.replace("@", "")
    await state.clear()

    worker = Worker.get(worker_id=message.from_user.id)

    if worker is not None:
        return

    user = Userx.get(user_login=username.lower())

    if user is None:
        await message.answer(ded(f"""
            ❌ Пользователь `<code>@{username}</code>` не найден в боте. Попробуйте еще раз.
        """))
        await state.set_state("admin_add_name")
        return

    if user.user_id == message.from_user.id:
        await message.answer(ded(f"""
                ❌ Вы владелец и не можете добавить себя в воркеры. Попробуйте еще раз.
            """))
        await state.set_state("admin_add_name")
        return

    await message.answer(ded("""
            📌 Введите заметку для воркера: 
        """), reply_markup=admin_back())

    await state.update_data(username=username.lower())
    await state.set_state("admin_add_prefix")


@router.message(F.text, StateFilter("admin_add_prefix"))
async def admin_add_prefix(message: Message, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    username = (await state.get_data())['username']
    prefix = message.text
    await state.clear()

    worker = Worker.get(worker_id=message.from_user.id)

    if worker is not None:
        return

    user = Userx.get(user_login=username)

    Worker.add(
        worker_id=user.user_id,
        worker_prefix=prefix,
    )

    await message.answer(ded(f"""
                ✅ <b>Воркер успешно добавлен.</b>
                
                📌 Префикс: <code>{prefix}</code>
                👤 Пользователь: @{user.user_login} ({user.user_id})
            """), reply_markup=admin_back())

    await state.set_state("admin_add_prefix")


@router.callback_query(F.data == "admin_list")
async def admin_list(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    await state.clear()

    await call.message.edit_text(ded(f"""
            📋 Выберите воркера из списка ниже для редактирования.
            
            ⚠️ В этом списке не отображаются создатели бота. Измените их в конфиге бота
        """), reply_markup=admin_markup_list())


@router.callback_query(F.data == "add_stats")
async def add_stats(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    await state.clear()

    await call.message.edit_text(ded(f"""
            💬 <b>Введите количество успешных сделок которое будет отображаться у вас в профиле:</b> 
        """), reply_markup=admin_back())

    await state.set_state("get_add_stat_sdels")


@router.callback_query(F.data == "admin_deals")
async def add_stats(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    await state.clear()

    worker = Worker.get(worker_id=call.from_user.id)

    deals_count = 0

    for deal in Deals.get_all():
        if (worker is None and worker is None) or \
                (worker is not None and deal.deal_member == worker.worker_id):
            deals_count += 1
    await call.message.edit_text(ded(f"""
            📈 Выберите сделку ({deals_count})
            
            ⚠️ Показываются последние 30 сделок.
            ⚠️ Показываются только сделки где вы являетесь участником.
        """), reply_markup=select_deals(worker, worker is None))


@router.message(F.text, StateFilter("get_add_stat_sdels"))
async def get_add_stat_sdels(message: Message, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    sucessful_deals = message.text
    await state.clear()

    Userx.update(user_id=message.from_user.id, sucessful_deals=sucessful_deals)
    await message.answer(ded(f"""
            ✅ <b>Количество успешных сделок в профиле успешно изменено</b>
        """))

    await state.clear()


@router.callback_query(F.data.startswith("admin_workers_page"))
async def admin_workers_page(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    page = call.data.split(":")[1]
    await state.clear()

    await call.message.edit_text(ded(f"""
        📋 Выберите воркера из списка ниже для редактирования.
            
        ⚠️ В этом списке не отображаются создатели бота. Измените их в конфиге бота
    """), reply_markup=admin_markup_list(int(page)))




@router.callback_query(F.data.startswith("select_worker:"))
async def select_worker(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    worker_id = call.data.split(":")[1]
    await state.clear()

    worker = Worker.get(worker_id=worker_id)
    worker_user = Userx.get(user_id=worker_id)
    how_days = int(get_unix() - worker.worker_set_unix) // 60 // 60 // 24

    await call.message.edit_text(ded(f"""
                👤 <b>Воркер @{worker_user.user_login} <b>({worker.worker_id})</b> - №{worker.increment}</b>
                
                📌 <b>Префикс:</b> {worker.worker_prefix}.
                
                🕘 <b>Добавлен:</b> {convert_date(worker.worker_set_unix, True, False)}.
                
                ✅ <b>Успешных сделок:</b> {worker.worker_deals_sucessful}.
                
                ❌ <b>Отмененных сделок:</b> {worker.worker_deals_cancel}.
        """), reply_markup=worker_edit(worker_id))


@router.callback_query(F.data.startswith("worker_delete:"))
async def select_worker(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    worker_id = call.data.split(":")[1]
    await state.clear()

    worker = Worker.get(worker_id=call.from_user.id)

    if worker is not None:
        return

    Worker.delete(worker_id=worker_id)

    await call.answer("❌ Воркер удален")

    await back_admin(call, bot, state, arSession, i18n)


@router.callback_query(F.data.startswith("edit_deal:"))
async def edat_deal(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    deal_id = call.data.split(":")[1]
    await state.clear()

    deal = Deals.get(deal_id=deal_id)

    if deal is None:
        await call.answer("❌ Данная сделка уже удалена.", show_alert=True)
        return

    if is_wallet_ton(deal.deal_address):
        deal_owner = Userx.get(user_ton_wallet=deal.deal_address)
    else:
        deal_owner = Userx.get(user_card_wallet=deal.deal_address)
    deal_member = Userx.get(user_id=deal.deal_member)

    await call.message.edit_text(ded(f"""
            💼 Сделка #{deal.deal_id}
            
            📌 Продавец:
            👤 {deal_owner.user_name} (<code>{deal_owner.user_id}</code>)
            • Юзернейм: @{deal_owner.user_login}
            
            📌 <b>Покупатель:</b>
            {f'''
            👤 {deal_member.user_name} (<code>{deal_member.user_id}</code>)
            • Юзернейм: @{deal_member.user_login}
            ''' if deal_member is not None else 'Не установлен'}
            
            ✉️ <b>Описание сделки</b>: {deal.deal_description}
            
            💰 <b>Сумма</b>: {deal.deal_amount} {deal.deal_currency.upper()}
        """), reply_markup=edit_deal(deal.deal_id))


@router.callback_query(F.data.startswith("cancel_deal:"))
async def cancel_deal(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    deal_id = call.data.split(":")[1]
    await state.clear()

    deal = Deals.get(deal_id=deal_id)

    if deal is None:
        await call.answer("❌ Данная сделка уже удалена", True)
        return

    Deals.update(deal_id=deal_id, deal_status="pending delete")
    Deals.delete(deal_id=deal_id)

    await call.message.edit_text(
        "✅ Сделка успешно удалена",
        reply_markup=admin_back()
    )


@router.callback_query(F.data.startswith("confirm_deal:"))
async def confirm_deal(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    deal_id = call.data.split(":")[1]
    await state.clear()

    deal = Deals.get(deal_id=deal_id)
    if is_wallet_ton(deal.deal_address):
        deal_owner = Userx.get(user_ton_wallet=deal.deal_address)
    else:
        deal_owner = Userx.get(user_card_wallet=deal.deal_address)

    deal_member = Userx.get(user_id=deal.deal_member)

    if deal is None:
        await call.answer("❌ Данная сделка уже удалена", True)
        return

    if deal_member is None:
        await call.answer("❌ Для подтверждения сделки нужно чтобы в ней был покупатель.", True)
        return

    if deal.deal_status == "paided":
        await call.answer("❌ Данная сделка уже оплачена.", True)
        return

    Deals.update(deal_id=deal_id, deal_status="paided")

    try:
        await call.answer("✅ Оплата для сделки успешно подтверждена.")
        await call.message.edit_text(ded(f"""
            ✅ Оплата для сделки успешно подтверждена.
        """), reply_markup=admin_back())

        await bot.send_message(
            chat_id=deal_owner.user_id,
            text=i18n.get("deal_paid", deal_id=deal.deal_id, deal_description=deal.deal_description,
                          deal_member_username=deal_member.user_login),
            reply_markup=deal_confirmed(i18n, f"https://t.me/{deal_member.user_login}", deal.deal_id)
        )

        await bot.send_message(
            chat_id=deal_member.user_id,
            text=i18n.get("deal_paid_member", deal_id=deal.deal_id),
            reply_markup=back_menu(i18n)
        )
    except:
        Deals.delete(deal_id=deal_id)
        await call.message.answer(" К сожалению не удалось подтвердить оплату для сделки.", reply_markup=admin_back())
        await call.message.delete()
