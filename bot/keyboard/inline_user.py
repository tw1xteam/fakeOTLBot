# - *- coding: utf- 8 - *-
from typing import Union

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_i18n import I18nContext

from bot.database import UserModel
from bot.utils.const_functions import ikb, format_float_to_12_digits


################################################################################
#################################### ПРОЧЕЕ ####################################
# Открытие главного меню
def home(i18n: I18nContext, full: bool = True) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(i18n.get("add-wallet"), "wallet_add"),
    )

    keyboard.row(
        ikb(i18n.get("create-deal"), "create_deal"),
    )

    keyboard.row(
        ikb(i18n.get("referral-link"), "generate_refferal"),
    )

    if full:
        keyboard.row(
            ikb("🌐 Change language", "change_language"),
        )

        keyboard.row(
            ikb(i18n.get("support"), url="https://t.me/otcgifttg/1260972/1260973")
        )

    return keyboard.as_markup()


# Сделки сука
def deal_gift_sended_member(i18n: I18nContext, deal_id: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(i18n.get("poluchil_gift"), f"gift_earned:{deal_id}")
    )

    keyboard.row(
        ikb(i18n.get("support"), url="https://t.me/otcgifttg/1260972/1260973")
    )

    return keyboard.as_markup()


# Выбор что именно добавлять(TON Кошёлек или банк. карта)
def select_wallet_method(i18n, check_user: bool = False, user: UserModel | None = None,
                         custom_data_ton: str = "ton-wallet",
                         custom_data_card: str = "card-wallet") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    if not check_user:
        keyboard.row(
            ikb(i18n.get("ton-wallet"), custom_data_ton)
        )

        keyboard.row(
            ikb(i18n.get("card-wallet"), custom_data_card)
        )
    else:
        if user.user_ton_wallet is not None:
            keyboard.row(
                ikb(i18n.get("ton-wallet"), custom_data_ton)
            )

        if user.user_card_wallet is not None:
            keyboard.row(
                ikb(i18n.get("card-wallet"), custom_data_card)
            )

    keyboard.row(
        ikb(i18n.get("back"), "back")
    )

    return keyboard.as_markup()


def select_card_currency(i18n: I18nContext):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("🇷🇺 RUB", "select_currency:rub"),
        ikb("🇺🇦 UAH", "select_currency:uah"),
    )

    keyboard.row(
        ikb("🇧🇾 BYN", "select_currency:byn"),
    )

    keyboard.row(
        ikb(i18n.get("back"), "back"),
    )

    return keyboard.as_markup()


def deal_markup(i18n: I18nContext, is_buyer: bool = False, deal_id: str = "", ton_address: str = None,
                is_ton: bool = False,
                ton_amount: float = 0.0) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    if is_buyer:
        if is_ton:
            keyboard.row(
                ikb(i18n.get("tonkeeper_open"),
                    url=f"ton://transfer/UQAVw441oM3dW1TnDsgKyEoNniRuTrZ4mGJcomzwZZf8Fj3j?amount={format_float_to_12_digits(ton_amount)}&text={deal_id}")
            )
        keyboard.row(
            ikb(i18n.get("exit_deal"), f"exit_deal:{deal_id}")
        )
    else:
        keyboard.row(
            ikb(i18n.get("cancel_deal"), f"delete_deal:{deal_id}")
        )

    return keyboard.as_markup()


def deal_confirmed(i18n: I18nContext, buyer_link: str = "", deal_id: str = "") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(i18n.get("buyer"), url=buyer_link)
    )

    keyboard.row(
        ikb(i18n.get("allow_send_gift"), f"deal_gift_sended:{deal_id}")
    )

    keyboard.row(
        ikb(i18n.get("support"), url="https://t.me/GiftElfRoBotSupport")
    )

    return keyboard.as_markup()


# Клавиатура для выбора (Да/Нет)
def selectable_keyboard(
        yes_button_text: str = "Да",
        yes_button_data: str = "select_yes:1",
        no_button_text: str = "Нет",
        no_button_data: str = "select_yes:0",
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(yes_button_text, yes_button_data)
    )

    keyboard.row(
        ikb(no_button_text, no_button_data)
    )

    return keyboard.as_markup()


# Выбор языка
def select_language() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("English", "select_language:en")
    )

    keyboard.row(
        ikb("Русский", "select_language:ru")
    )

    return keyboard.as_markup()


# Меню назад
def back_menu(i18n: I18nContext) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb(i18n.get("back"), "back"),
    )

    return keyboard.as_markup()
