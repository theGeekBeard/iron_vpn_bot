import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, PreCheckoutQuery, ContentTypes, \
    Message, MediaGroup
from aiogram.utils.exceptions import BotBlocked

from data.callback_data import tariff_cd, tariff_cd_
from data.config import PAYMENT_TOKEN, VIDEOS, ADMINS
from handlers.users.menu.balance import top_up
from keyboards.inline.inline import menuMarkup
from loader import dp, bot, db
from utils.getter_key import get_key


@dp.callback_query_handler(tariff_cd.filter(), state="*")
async def get_invoice(call: CallbackQuery, state: FSMContext, callback_data: dict = None):
    tariff_id = int(callback_data["tariff_id"])

    keys = await get_key(tariff_id)

    if not keys:
        return await call.answer(
            "🥺 К сожалению, в данный момент в наличии нет ключей для этого тарифа\n\n⏳ Попробуйте позже",
            show_alert=True)

    tariff = await db.get_tariff(tariff_id)

    async with state.proxy() as data:
        data["tariff_id"] = tariff_id

    if tariff_id == 1:
        return await buy_handler(call.message, state)

    price = str(tariff[0]['price'])
    tariff_name = f"{tariff[0]['name']} — {price}₽"

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("💳 Оплатить", pay=True)],
        [InlineKeyboardButton("⬅️ Назад", callback_data="tariffs")]
    ])

    await bot.send_invoice(call.from_user.id, title="Оплата тарифа", description=tariff_name,
                           payload="buy", provider_token=PAYMENT_TOKEN, currency="RUB",
                           start_parameter=call.from_user.id,
                           prices=[{"label": "Руб", "amount": int(price + "00")}], reply_markup=markup)

    try:
        await call.message.delete()
    except:
        pass


@dp.callback_query_handler(tariff_cd_.filter(), state="*")
async def get_invoice(call: CallbackQuery, state: FSMContext, callback_data: dict = None):
    tariff_id = int(callback_data["tariff_id"])
    user = await db.get_user(call.message.chat.id)
    balance = user[0]["balance"]

    keys = await get_key(tariff_id)

    if not keys:
        return await call.answer(
            "🥺 К сожалению, в данный момент в наличии нет ключей для этого тарифа\n\n⏳ Попробуйте позже",
            show_alert=True)

    tariff = await db.get_tariff(tariff_id)

    price = tariff[0]['price']
    if balance < price:
        return await call.answer(
            "🥺 К сожалению, не хватает средств\n\n⏳ Пополните свой баланс",
            show_alert=True)

    async with state.proxy() as data:
        data["tariff_id"] = tariff_id

    await db.update_user_info(call.message.chat.id, {
        "balance": user[0]["balance"] - price
    })

    await buy_handler(call.message, state)


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message, state: FSMContext):
    payload = message.successful_payment.invoice_payload

    if payload == "buy":
        await buy_handler(message, state)
    else:
        await top_up(message, state)


async def buy_handler(message: types.Message, state: FSMContext):
    user_id = message.chat.id

    msg = []

    text = """<b>Тариф оплачен!</b>

Ключи находятся выше ⬆️

<i>это ваш ключ 🔑
ни с кем не делитесь ключом.
он - индивидуальный!

<u>инструкция по установке находится в разделе "Помощь"</u></i>"""

    async with state.proxy() as data:
        tariff_id = data["tariff_id"]

    keys = await get_key(tariff_id)

    file_path1 = keys["file_path"]
    image_path1 = keys["image_path"]

    file1 = open(file_path1, 'rb')
    qr_code1 = open(image_path1, 'rb')

    qr_code_msg1 = await message.answer_photo(qr_code1)
    msg.append(qr_code_msg1.message_id)
    if tariff_id != 4:
        file_msg1 = await message.answer_document(file1, caption=text, reply_markup=menuMarkup)
    else:
        file_msg1 = await message.answer_document(file1)
        msg.append(file_msg1.message_id)

    qr_code_file_id1 = qr_code_msg1.photo[-1].file_id
    file_file_id1 = file_msg1.document.file_id

    vpn1 = await db.add_vpn(file_file_id1, qr_code_file_id1, user_id)

    vpn_id1 = vpn1.data[0]["id"]

    vpn_id2 = None

    if tariff_id == 4:
        file_path2 = keys["file_path2"]
        image_path2 = keys["image_path2"]

        file2 = open(file_path2, 'rb')
        qr_code2 = open(image_path2, 'rb')

        qr_code_msg2 = await message.answer_photo(qr_code2)
        msg.append(qr_code_msg2.message_id)
        file_msg2 = await message.answer_document(file2, caption=text, reply_markup=menuMarkup)

        qr_code_file_id2 = qr_code_msg2.photo[-1].file_id
        file_file_id2 = file_msg2.document.file_id

        vpn2 = await db.add_vpn(file_file_id2, qr_code_file_id2, user_id)

        vpn_id2 = vpn2.data[0]["id"]

    tariff = await db.get_tariff(tariff_id)
    price = tariff[0]["price"]
    term = tariff[0]["term"]
    tariff_name = f"{tariff[0]['name']} — {price}₽"

    await db.update_user_info(user_id, {"vpn_id": vpn_id1, "vpn_id2": vpn_id2, "term": term, "paid": True})

    await db.add_new_payment(message.chat.id, price, "Оплата тарифа")
    await db.add_new_payment(message.chat.id, 0, "Конфиг создан")

    for admin in ADMINS:
        text = f"""<b>💰 Новая оплата 💰</b>

ID: {user_id}
<b>Пользователь:</b> @{message.chat.username}
<b>Имя:</b> {message.chat.full_name}

<b>Тариф:</b> {tariff_name}
<b>Сумма оплаты:</b> {price}"""

        if tariff_id == 4:
            media = MediaGroup()
            media.attach_document(file_file_id1)
            media.attach_document(file_file_id2, caption=text)
            await bot.send_media_group(admin, media)
        else:
            await bot.send_document(admin, file_file_id1, caption=text)

    user = await db.get_user(user_id)

    referral = user[0]['referal']
    if referral:
        ref_user = await db.get_user(referral)
        amount = price * 15 // 100
        await db.update_user_info(referral, {"balance": ref_user[0]["balance"] + amount})

        try:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton("✅ Хорошо", callback_data="ok")]
            ])
            await bot.send_message(referral, f"🥳 Ваш реферал совершил покупку. На Ваш баланс начислено {amount}₽",
                                   reply_markup=markup)
        except BotBlocked:
            pass

    async with state.proxy() as data:
        data["msg"] = msg

    file1.close()
    qr_code1.close()
    # os.remove(file_path1)
    # os.remove(image_path1)

    if tariff_id == 4:
        file2.close()
        qr_code2.close()
        # os.remove(file_path2)
        # os.remove(image_path2)

    try:
        await message.delete()
        await bot.delete_message(user_id, message.message_id - 1)
    except:
        pass
