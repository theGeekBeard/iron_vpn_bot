from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.callback_data import tariff_cd
from loader import db

menuMarkup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("🔑 Мои ключи 🔑", callback_data="my_keys")],
    [InlineKeyboardButton("💰 Баланс", callback_data="balance"),
     InlineKeyboardButton("🗂 Тарифы", callback_data="tariffs")],
    [InlineKeyboardButton("🗓 История", callback_data="history"),
     InlineKeyboardButton("👥 Реф. программа", callback_data="referral")],
    [InlineKeyboardButton("🆘 Помощь", callback_data="help"),
     InlineKeyboardButton("📋 Оферта", callback_data="rules")],
])


async def create_tariffs_markup(user_id):
    user = await db.get_user(user_id)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("☘️ Lite VPN — 4₽ / день", url="https://t.me/lite_vpn_bot")]
    ])

    tariffs = await db.get_tariffs()

    index = 0
    if tariffs[0]["id"] == 1:
        index = 1
        if not (user and user[0]["vpn_id"]):
            markup.row(InlineKeyboardButton("🇱🇻 Пробный ключ 🔑", callback_data=tariff_cd.new(tariff_id=1)))

    for tariff in tariffs[index:]:
        tariff_id = tariff["id"]
        price = tariff['price']
        tariff_name = f"{tariff['name']} — {price}₽"

        markup.row(InlineKeyboardButton(tariff_name, callback_data=tariff_cd.new(tariff_id=tariff_id)))

    markup.row(InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))

    return markup
