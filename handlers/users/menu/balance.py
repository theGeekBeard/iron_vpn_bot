from random import randint
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ContentTypes

from data.callback_data import amount_cd_, tariff_cd_
from data.config import amounts, ADMINS, PAYMENT_TOKEN
from loader import dp, db, bot
from utils.getter_key import get_key


@dp.callback_query_handler(text="balance", state="*")
async def get_balance(call: Union[CallbackQuery, types.Message], state: FSMContext):
    if isinstance(call, CallbackQuery):
        user = await db.get_user(call.message.chat.id)
    else:
        message = call
        user = await db.get_user(message.chat.id)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("➕ Пополнить баланс", callback_data="top_up_balance")],
        [InlineKeyboardButton("🔑 Купить ключ за баланс", callback_data="buy_key_balance")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")]
    ])

    text = f"""<b>💰 Ваш баланс: {user[0]["balance"]}₽</b>"""

    if isinstance(call, CallbackQuery):
        try:
            await call.message.edit_text(text, reply_markup=markup, parse_mode="HTML")
        except:
            message = call.message
            await message.answer(text, reply_markup=markup, parse_mode="HTML")
            try:
                await message.delete()
            except:
                pass
    else:
        message = call
        await message.answer(text, reply_markup=markup, parse_mode="HTML")
        try:
            await message.delete()
        except:
            pass

    async with state.proxy() as data:
        if "msg" in data.keys():
            msg = data["msg"]
            for m in msg:
                try:
                    await bot.delete_message(call.message.chat.id, m)
                except:
                    pass
            data.pop("msg")


@dp.callback_query_handler(text="buy_key_balance")
async def buy_key_balance(call: CallbackQuery, state: FSMContext):
    tariffs = await db.get_tariffs()

    markup = InlineKeyboardMarkup()

    index = 0
    if tariffs[0]["id"] == 1:
        index = 1

    for tariff in tariffs[index:]:
        tariff_id = tariff["id"]
        price = tariff['price']
        tariff_name = f"{tariff['name']} — {price}₽"

        markup.row(InlineKeyboardButton(tariff_name, callback_data=tariff_cd_.new(tariff_id=tariff_id)))

    markup.row(InlineKeyboardButton("⬅️ Назад", callback_data="balance"))
    markup.row(InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))

    text = """Выберите тариф ⤵️"""

    await call.message.edit_text(text, reply_markup=markup)


@dp.callback_query_handler(text="top_up_balance")
async def top_up_balance(call: CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(f"{amounts[1]}₽", callback_data=amount_cd_.new(amount=amounts[1])),
         InlineKeyboardButton(f"{amounts[2]}₽", callback_data=amount_cd_.new(amount=amounts[2])),
         InlineKeyboardButton(f"{amounts[3]}₽", callback_data=amount_cd_.new(amount=amounts[3])),
         InlineKeyboardButton(f"{amounts[4]}₽", callback_data=amount_cd_.new(amount=amounts[4]))],
        [InlineKeyboardButton("⬅️ Назад", callback_data="balance")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ])

    text = """Выберите сумму для пополнения ⤵️"""

    try:
        await call.message.edit_text(text, reply_markup=markup)
    except:
        await call.message.answer(text, reply_markup=markup)
        try:
            await call.message.delete()
        except:
            pass


@dp.callback_query_handler(amount_cd_.filter())
async def get_payment_link(call: CallbackQuery, state: FSMContext, callback_data: dict):
    amount = int(callback_data["amount"])

    async with state.proxy() as data:
        data["amount"] = amount

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(f"💳 Оплатить", pay=True)],
        [InlineKeyboardButton("⬅️ Назад", callback_data="top_up_balance")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ])

    await bot.send_invoice(call.from_user.id, title="Пополнение баланса",
                           description=f"пополнение баланса на {amount}₽",
                           payload="top_up", provider_token=PAYMENT_TOKEN, currency="RUB",
                           start_parameter=call.message.chat.id,
                           prices=[{"label": "Руб", "amount": int(str(amount) + "00")}], reply_markup=markup)

    await call.message.delete()


async def top_up(message: types.Message, state: FSMContext):
    await get_balance(message, state)

    async with state.proxy() as data:
        amount = data["amount"]

    user_id = message.chat.id

    user = await db.get_user(user_id)

    await db.update_user_info(user_id, {
        "balance": user[0]["balance"] + amount
    })

    await db.add_new_payment(user_id, amount, "Пополнение баланса")

    for admin in ADMINS:
        await bot.send_message(admin, f"""💰 Пополнение баланса 💰
Сумма: {amount}

ID: {user_id}
Username: @{message.chat.username}
Имя пользователя: {message.chat.full_name}""")
