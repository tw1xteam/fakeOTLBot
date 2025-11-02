welcome-message =
    <b>👋 Welcome to ELF OTC - a reliable P2P guarantor</b>

    <b>💼 Buy and sell anything - safely!</b>
    From Telegram gifts and NFTs to tokens and fiat, transactions are easy and risk-free.

    🔹 Convenient wallet management
    🔹 Referral system

    <b>📖 How to use it?</b>
    Read the instructions — https://t.me/otcgifttg/71034/71035

    Select the desired section below:

add-wallet-ton-exists =
    💼 <b>Your current wallet</b>: <code>{ $wallet }</code>

    Send a new wallet address to update it or press the button below to return to the menu.

add-wallet-ton-not-exists =
    🔑 <b>Add your TON wallet:</b>

    Please send your wallet address.

referral-link-text =
    🔗 <b>Your referral link:</b>

    <code>https://t.me/{ $bot_username }?start=ref={ $user_wallet} </code>

    👥 <b>Referral count:</b> { $referral_count }
    💰 <b>Referral earnings:</b> { $referral_earnings } TON
    40% of bot fees

add-wallet-card-exists =
    🔑 <b>Your current card:</b> <code>{ $wallet }</code>

    Send a new card to update or click the button below to return to the menu.

add-wallet-card-not-exists =
    💳 <b>Add your bank card:</b>

    Please send your card number (16 digits).

deals_create =
    💼 <b>Create a Deal</b>

    Enter the deal amount in { $format } <code>100.5</code>

deal_description =
    📝 <b>Provide details for this deal:</b>

    Example: <code>10 caps and Pepe...</code>

select_payment_method =
    💰 <b>Select payment method:</b>

sucessful_create_deal =
    ✅ <b>Deal successfully created!</b>

    💰 <b>Amount:</b> <code>{ $deal_amount } { $deal_amount_format}</code>
    📜 <b>Description:</b> <code>{ $deal_description }</code>
    🔗 <b>Buyer Link</b>: https://t.me/{ $bot_username}?start={ $deal_id}

joined_to_deal =
    User @{ $username } ({ $user_id }) joined deal #{ $deal_id }
    • Successful deals: { $deals_count }

deal_info =
    💳 <b>Deal Information</b> #{ $deal_id }

    👤 <b>You are the buyer</b> in this deal.
    📌 Seller: @{ $username } (<b>{ $user_id }</b>)
    • Successful deals: { $deals_count }

    • You are buying: { $deal_description }

    { $paid_text }

    💰 <b>Amount to pay:<b> <code>{ $deal_amount }</code> { $currency }

    📝 <b>Payment comment:</b> <code>{ $deal_id }</code>

    ⚠️ <b>Please make sure the data is correct before payment. Comment(memo) is required!</b>

    After payment, expect an automatic confirmation

deal_paid =
    ✅ <b>Payment confirmed for deal #{ $deal_id }</b>

    Description: { $deal_description }

    Send the gift to the buyer — @{ $deal_member_username }

    ⚠️ Only send the gift to the person specified here. If you send the gift to someone else, no refund will be issued. Be sure to record a video of the handover.

deal_paid_member =
    ✅ <b>Payment confirmed</b> for deal #{ $deal_id }

    Please confirm receipt of the gift once the seller sends it.

deal_gift_sended =
    ✅ The seller has confirmed gift shipment. Waiting for buyer's confirmation

deal_gift_sended_member =
    🎁 Продавец @{ $deal_owner_username } отправил подарок. Пожалуйста, подтвердите его получение.

cancel_deal_text =
    ❌ Are you sure you want to cancel deal #{ $deal_id }?

    This action cannot be undone.

exit_deal_text =
    ❓ Are you sure you want to exit deal #{ $deal_id }?

    This will notify the seller, and the deal will revert to its initial state.

add-wallet = 🪙 Add/Change Wallet
ton-wallet = 💎 TON-Wallet
card-wallet = 💳 Card
create-deal = 📄 Create a Deal
referral-link = 🧷 Referral Link
support = 📞 Support
back = 🔙 Back to Menu
wallet_specified = ❌ Please connect your wallet through the menu first.
incorrect_wallet = ❌ Invalid TON wallet format. Please try again.
incorrect_card_wallet = ❌ Invalid card format. Please try again.
invalid_amount_format = ❌ Invalid amount format. Please try again.
successful_wallet = ✅ Wallet successfully added/updated!
tonkeeper_open = Open in Tonkeeper
exit_deal = ❌ Exit Deal
cancel_deal = ❌ Cancel Deal
invalid_deal_id = ❌ Invalid deal ID.
own_deal_unsupport = ❌ You cannot participate in your own deal.
already_buyer = ❌ This deal already has a buyer. You cannot participate in it.
select_payment_country = 💳 <b>Select currency for card</b>
cancel_yes = ✅ Yes, Cancel
cancel_no = 🔙 No
deal_deleted = ✅ Deal successful canceled
deal_cancel_delete = ❌ Action canceled
deal_exited = ✅ Deal successful exited
exited_deal = User @{ $exit_username } ({ $exit_id }) exited deal #{ $deal_id }. The deal has reverted to its initial state.
buyer = 👤 Buyer
allow_send_gift = 🎁 Confirm gift shipment
deal_member_da = ✅ <b>The buyer has confirmed receipt of the gift(s)</b>
deal_ended_owner =
    ✅ <b>Deal #{ $deal_id } completed.</b>

    🤖 <b>Thank you for using our service.</b>

    💰 <b>Withdrawal to your specified payment details will be processed within 2-3 hours. This delay helps prevent fraudulent activity.</b>
deal_ended =
    ✅ <b>Deal #{ $deal_id } completed.</b>

    🤖 <b>Thank you for using our service.</b>
