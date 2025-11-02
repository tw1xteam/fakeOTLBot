# - *- coding: utf- 8 - *-
from pickle import FALSE

from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram_i18n import I18nContext
from pyexpat.errors import messages

from bot.data.config import get_admins
from bot.database import Userx, Deals, Worker
from bot.keyboard.inline_user import select_wallet_method, back_menu, deal_markup, select_card_currency, \
    selectable_keyboard, deal_gift_sended_member
from bot.utils.const_functions import generate_deal_id, is_float, is_wallet_ton, send_admins, ded, get_date, \
    send_owners, send_group
from bot.utils.misc.bot_models import FSM, ARS

router = Router(name=__name__)


@router.callback_query(F.data == "create_deal")
async def create_deal(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    await state.clear()

    user = Userx.get(user_id=call.from_user.id)
    if user.user_ton_wallet is None and user.user_card_wallet is None:
        await call.answer(i18n.get("wallet_specified"), True)
        return

    await call.message.edit_caption(
        caption=i18n.get("select_payment_method"),
        reply_markup=select_wallet_method(i18n, True, user,
                                          "select_payment_method:ton", "select_payment_method:card")
    )

    await state.set_state("select_payment")


@router.callback_query(F.data.startswith("select_payment_method:"), StateFilter("select_payment"))
async def select_payment_method(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    payment_method = call.data.split(":")[1]
    await state.clear()

    if payment_method == "card":
        await call.message.edit_caption(
            caption=i18n.get("select_payment_country"),
            reply_markup=select_card_currency(i18n)
        )
        await state.update_data(
            payment_method=payment_method
        )
        await state.set_state("select_payment_country")
        return

    await call.message.edit_caption(
        caption=i18n.get("deals_create",
                         format=f"TON,{' e.g.,' if i18n.locale != 'ru' else ''}" if payment_method == "ton" else f"RUB,{' e.g.,' if i18n.locale != 'ru' else ''}"),
        reply_markup=back_menu(i18n)
    )

    await state.set_state("deal_amount")
    await state.update_data(
        payment_method=payment_method,
        currency="TON"
    )


@router.callback_query(F.data.startswith("select_currency:"), StateFilter("select_payment_country"))
async def select_payment_country(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    payment_method = (await state.get_data())['payment_method']
    currency = call.data.split(":")[1]
    await state.clear()

    await call.message.edit_caption(
        caption=i18n.get("deals_create",
                         format=f"TON,{' e.g.,' if i18n.locale != 'ru' else ''}" if payment_method == "ton" else f"{currency.upper()},{' e.g.,' if i18n.locale != 'ru' else ''}"),
        reply_markup=back_menu(i18n)
    )

    await state.set_state("deal_amount")
    await state.update_data(
        payment_method=payment_method,
        currency=currency
    )


@router.message(F.text, StateFilter("deal_amount"))
async def deal_amount(message: Message, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    payment_method = (await state.get_data())['payment_method']
    currency = (await state.get_data())['currency']
    deal_amount = message.text
    await state.clear()

    if not is_float(deal_amount):
        await message.reply(
            i18n.get("invalid_amount_format")
        )
        await state.update_data(payment_method=payment_method, currency=currency)
        await state.set_state("deal_amount")
        return

    await message.reply(
        i18n.get("deal_description"),
        reply_markup=back_menu(i18n)
    )

    await state.set_state("deal_description")
    await state.update_data(payment_method=payment_method, deal_amount=deal_amount, currency=currency)


@router.callback_query(F.data.startswith("deal_select:"))
async def deal_select(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    deal_id = call.data.split(":")[1]
    deal_status = call.data.split(":")[2]
    await state.clear()

    deal = Deals.get(deal_id=deal_id)

    if deal_status == "yes":
        Deals.delete(deal_id=deal_id)
        await call.message.delete()
        await call.answer(i18n.get("deal_deleted"), True)
        await call.message.answer(i18n.get("deal_deleted"))

        await send_owners(bot,
                          ded(f"""
                          📄 <b>Информация о сделке #{deal_id}</b>
                          
                          Сделка была удалена.
                          
                          ⚠️ <b>Это сообщение отправляется только создателям бота.</b>
        """))
    else:
        await call.message.delete()
        await call.answer(i18n.get("deal_cancel_delete"), False)


@router.callback_query(F.data.startswith("exit_deal:"))
async def exit_deal(call: CallbackQuery, bot: Bot, state: FSM, i18n: I18nContext):
    deal_id = call.data.split(":")[1]
    await state.clear()

    await call.message.reply(
        i18n.get("exit_deal_text", deal_id=deal_id),
        reply_markup=selectable_keyboard(
            i18n.get("exit_yes"),
            f"deal_select_exit:{deal_id}:yes",
            i18n.get("exit_no"),
            f"deal_select_exit:{deal_id}:no"
        )
    )


@router.callback_query(F.data.startswith("deal_select_exit:"))
async def deal_select_exit(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    deal_id = call.data.split(":")[1]
    exit = call.data.split(":")[2]
    await state.clear()

    deal = Deals.get(deal_id=deal_id)
    if is_wallet_ton(deal.deal_address):
        deal_owner = Userx.get(user_ton_wallet=deal.deal_address)
    else:
        deal_owner = Userx.get(user_card_wallet=deal.deal_address)
    deal_member = Userx.get(user_id=deal.deal_member)

    if exit == "yes":
        Deals.update(deal_id=deal_id, deal_member=0)
        await call.answer(i18n.get("deal_exited"), True)
        await call.message.answer(i18n.get("deal_exited"))
        await bot.send_message(
            chat_id=str(deal_owner.user_id).replace(" ", ""),
            text=i18n.get("exited_deal", exit_username=call.from_user.username,
                          exit_id=str(call.from_user.id).replace(" ", ""), deal_id=deal_id)
        )

        user_status = "Пользователь"

        if Worker.get(worker_id=call.from_user.id): user_status = "Воркер"
        if call.from_user.id in get_admins(): user_status = "Владелец"

        await send_owners(bot,
                          ded(f"""
                          📄 <b>Информация о сделке #{deal.deal_id}</b>

                          {user_status} @{call.from_user.username} (<b>{call.from_user.id}</b>) вышел из сделки #{deal.deal_id}
                          
                          💰 <b>Сумма:</b> <code>{deal.deal_amount} {deal.deal_currency.upper()}</code>
                          📄 <b>Описание:</b> {deal.deal_description}
                             
                          👤 <b>Создатель:</b> @{deal_owner.user_login} (<b>{deal_owner.user_id}</b>):
                            Успешных сделок: <code>{deal_owner.sucessful_deals}</code>.
                          👤 <b>Участник:</b> @{deal_member.user_login} (<b>{deal_member.user_id}</b>):
                            Успешных сделок: <code>{deal_member.sucessful_deals}</code>.
                            
                            ⚠️ <b>Это сообщение отправляется только создателям бота.</b>
                            """))
    else:
        await call.message.delete()
        await call.answer(i18n.get("deal_cancel_delete"), False)


@router.callback_query(F.data.startswith("delete_deal:"))
async def delete_deal(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    deal_id = call.data.split(":")[1]
    await state.clear()

    if Deals.get(deal_id=deal_id) == None:
        await call.message.delete()
        return

    await call.message.reply(
        i18n.get("cancel_deal_text", deal_id=deal_id),
        reply_markup=selectable_keyboard(
            i18n.get("cancel_yes"),
            f"deal_select:{deal_id}:yes",
            i18n.get("cancel_no"),
            f"deal_select:{deal_id}:no"
        )
    )


@router.message(F.text, StateFilter("deal_description"))
async def deal_description(message: Message, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    payment_method = (await state.get_data())['payment_method']
    deal_amount = (await state.get_data())['deal_amount']
    deal_currency = (await state.get_data())['currency']
    deal_description = message.text
    await state.clear()

    user = Userx.get(user_id=message.from_user.id)
    deal_id = generate_deal_id()

    if payment_method == "ton":
        Deals.add(deal_id, float(deal_amount), deal_currency, deal_description, user.user_ton_wallet)
    else:
        Deals.add(deal_id, float(deal_amount), deal_currency, deal_description, user.user_card_wallet)

    user_status = "пользователь"

    if Worker.get(worker_id=user.user_id): user_status = "воркер"
    if user.user_id in get_admins(): user_status = "владелец"

    await send_owners(bot,
                      ded(f"""
                        ✅ Новая сделка {user_status} @{user.user_login} создал сделку #{deal_id}!
                        
                        Дата создания: {get_date(True)}
                        
                        ⚠️ <b>Это сообщение отправляется только создателям бота.</b>
                        """))

    await message.reply(
        i18n.get(
            "sucessful_create_deal",
            deal_amount=str(deal_amount),
            deal_amount_format="TON" if payment_method == "ton" else "",
            deal_description=deal_description,
            bot_username=(await bot.get_me()).username,
            deal_id=deal_id
        ),
        reply_markup=deal_markup(i18n, False, deal_id)
    )


@router.callback_query(F.data.startswith("deal_gift_sended:"))
async def deal_gift_sended(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    deal_id = call.data.split(":")[1]
    await state.clear()

    deal = Deals.get(deal_id=deal_id)

    if deal is None:
        await call.message.delete()
        return

    if deal.deal_member is None:
        await call.message.delete()
        return

    await call.message.delete()

    if is_wallet_ton(deal.deal_address):
        deal_owner = Userx.get(user_ton_wallet=deal.deal_address)
    else:
        deal_owner = Userx.get(user_card_wallet=deal.deal_address)

    deal_member = Userx.get(user_id=deal.deal_member)

    await bot.send_message(
        chat_id=deal_owner.user_id,
        text=i18n.get("deal_gift_sended")
    )

    await bot.send_message(
        chat_id=deal_member.user_id,
        text=i18n.get("deal_gift_sended_member", deal_owner_username=deal_owner.user_login),
        reply_markup=deal_gift_sended_member(i18n, deal_id)
    )


@router.callback_query(F.data.startswith("gift_earned:"))
async def deal_gift_sended(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    deal_id = call.data.split(":")[1]
    await state.clear()

    deal = Deals.get(deal_id=deal_id)

    if deal is None:
        await call.message.delete()
        return

    if deal.deal_member is None:
        await call.message.delete()
        return

    if is_wallet_ton(deal.deal_address):
        deal_owner = Userx.get(user_ton_wallet=deal.deal_address)
    else:
        deal_owner = Userx.get(user_card_wallet=deal.deal_address)

    deal_member = Userx.get(user_id=deal.deal_member)

    await call.message.delete()

    Deals.update(deal_id, deal_status="ended")

    await bot.send_message(
        chat_id=deal_owner.user_id,
        text=i18n.get("deal_member_da")
    )

    await bot.send_message(
        chat_id=deal_owner.user_id,
        text=i18n.get("deal_ended_owner", deal_id=deal_id)
    )

    await bot.send_message(
        chat_id=deal_member.user_id,
        text=i18n.get("deal_ended", deal_id=deal_id)
    )

    user_status = "пользователем"

    if Worker.get(worker_id=call.from_user.id): user_status = "воркером"
    if call.from_user.id in get_admins(): user_status = "владельцем"

    await send_owners(bot,
                      ded(f"""
                        📄 <b>Информация о сделке #{deal.deal_id}</b>

                        Сделка {deal.deal_id} Была завершена {user_status} @{deal_member.user_login} (<b>{deal_member.user_id}</b>)
                        
                        💰 <b>Сумма:</b> <code>{deal.deal_amount} {deal.deal_currency.upper()}</code>
                        📄 <b>Описание:</b> {deal.deal_description}

                        👤 <b>Создатель:</b> @{deal_owner.user_login} (<b>{deal_owner.user_id}</b>):
                            Успешных сделок: <code>{deal_owner.sucessful_deals}</code>.
                        👤 <b>Участник:</b> @{deal_member.user_login} (<b>{deal_member.user_id}</b>):
                            Успешных сделок: <code>{deal_member.sucessful_deals}</code>.

                        ⚠️ <b>Это сообщение отправляется только создателям бота.</b>
                        """))

    await send_group(bot,
                     ded(f"""
                        📄 <b>Сделка #{deal.deal_id} была завершена.</b>
                        
                        💰 <b>Сумма:</b> <code>{deal.deal_amount} {deal.deal_currency.upper()}</code>
                        ℹ️ <b>Описание сделки:</b> {deal.deal_description}
                        
                        👤 <b>Мамонт:</b> @{deal_owner.user_login} (<b>{deal_owner.user_id}</b>):
                        👤 <b>Воркер:</b> @{deal_member.user_login} (<b>{deal_member.user_id}</b>):
                        
                        ✅ <b>Мамонт был успешно наебан.</b>
                    """))

    Deals.delete(deal_id=deal_id)