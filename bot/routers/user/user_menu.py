# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, FSInputFile, Message
from aiogram_i18n import I18nContext
from aiogram_i18n.types import InputMediaPhoto

from bot.data.config import GROUP_ID, TOPIC_ID
from bot.database import Userx
from bot.keyboard.inline_user import select_language, back_menu, select_wallet_method
from bot.routers.main_start import main_start
from bot.utils.const_functions import ded, validate_card
from bot.utils.misc.bot_models import FSM, ARS

router = Router(name=__name__)


@router.callback_query(F.data == "change_language")
async def choose_language(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    await state.clear()

    await call.message.reply(
        ded("""
            🌍 Choose your language:
            
            Выберите язык:
        """),
        reply_markup=select_language()
    )


@router.callback_query(F.data == "wallet_add")
async def wallet_add(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    await state.clear()

    await call.message.edit_caption(
        caption=i18n.get("select_payment_method"),
        reply_markup=select_wallet_method(i18n)
    )


@router.callback_query(F.data == "card-wallet")
async def wallet_add(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    await state.clear()

    user = Userx.get(user_id=call.from_user.id)

    await call.message.edit_caption(
        caption=i18n.get("add-wallet-card-not-exists") if user.user_card_wallet is None else i18n.get(
            "add-wallet-card-exists", wallet=user.user_card_wallet),
        reply_markup=back_menu(i18n)
    )

    await state.set_state("set_cardwallet")


@router.callback_query(F.data == "ton-wallet")
async def wallet_add(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    await state.clear()

    user = Userx.get(user_id=call.from_user.id)

    await call.message.edit_caption(
        caption=i18n.get("add-wallet-ton-not-exists") if user.user_ton_wallet is None else i18n.get(
            "add-wallet-ton-exists", wallet=user.user_ton_wallet),
        reply_markup=back_menu(i18n)
    )

    await state.set_state("set_tonwallet")


@router.message(F.text, StateFilter("set_tonwallet"))
async def set_ton_wallet(call: CallbackQuery, bot: Bot, state: FSM, i18n: I18nContext):
    message: str = call.text
    await state.clear()

    if len(message) < 34:
        await call.reply(i18n.get("incorrect_ton_wallet"))
        await state.set_state("set_tonwallet")
        return

    Userx.update(call.from_user.id, user_ton_wallet=message)

    await call.reply(i18n.get("successful_wallet"), reply_markup=back_menu(i18n))


@router.message(F.text, StateFilter("set_cardwallet"))
async def set_card_wallet(call: CallbackQuery, bot: Bot, state: FSM, i18n: I18nContext):
    message: str = call.text.replace(" ", "")
    await state.clear()

    if not message.isdigit() or len(message) < 16 or not validate_card(message):
        await call.reply(i18n.get("incorrect_card_wallet"))
        await state.set_state("set_cardwallet")
        return

    Userx.update(call.from_user.id, user_card_wallet=message)

    await call.reply(i18n.get("successful_wallet"), reply_markup=back_menu(i18n))


@router.callback_query(F.data.startswith("select_language:"))
async def change_language(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    locale = call.data.split(":")[1]
    await state.clear()

    try:
        await call.message.delete()
        await call.delete()
    except:
        ...

    await i18n.set_locale(locale)
    await main_start(call.message, bot, state, arSession, i18n)


@router.callback_query(F.data == "generate_refferal")
async def generate_refferal(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    await state.clear()

    user = Userx.get(user_id=call.from_user.id)
    if user.user_ton_wallet is None:
        await call.answer(i18n.get("wallet_specified"), True)
        return

    await call.message.reply(
        i18n.get("referral-link-text",
                 bot_username=(await bot.get_me()).username,
                 user_wallet=user.user_ton_wallet,
                 referral_count=user.refferal_count,
                 referral_earnings=0.0)
    )
