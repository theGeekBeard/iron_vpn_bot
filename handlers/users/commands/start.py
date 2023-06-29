import asyncio
from random import randint

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.exceptions import BotBlocked

from keyboards.inline.inline import create_tariffs_markup, menuMarkup
from loader import dp, db, bot


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()

    user_id = message.chat.id
    username = message.chat.username
    first_name = message.chat.first_name
    full_name = message.chat.first_name

    user = await db.get_user(user_id)

    if user:
        text = f"""👋 <b>Рады видеть вас снова, {first_name}!</b>

👤 <b>Ваш ID:</b> <code>{user_id}</code>"""

        if user[0]["vpn_id"]:
            term = user[0]["term"]
            text += f"\n⏳ <b>Дней до окончания подписки:</b> <code>{term}</code>\n\n<i>❗️ Если вы потеряли QR код или " \
                    f"конфиг файл - вы можете повторно их скачать в разделе 'Мои ключи'.</i>"
        else:
            text += "\n\n🥺 У вас пока нет ключей" \
                    "\n<i>Выберите нужный вам тариф в разделе 'Тарифы'</i>"

        markup = menuMarkup
    else:
        await db.add_new_user(user_id, username, full_name)

        start_command = message.text
        referer_id = start_command[7:]

        if referer_id:
            if referer_id != message.from_user.id:
                await db.update_user_info(user_id, {"referal": referer_id})

                try:
                    referer_user = await db.get_user(referer_id)
                    await db.update_user_info(referer_id, {"ref_count": referer_user[0]["ref_count"] + 1})

                    markup = InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton("✅ Хорошо", callback_data="ok")]
                    ])
                    await bot.send_message(referer_id, "По вашей реферальной ссылке присоединился пользователь!",
                                           reply_markup=markup)
                except BotBlocked:
                    pass

        text = f"""👋 <b>Привет, {first_name}!</b>

🚀 высокая скорость
💃🏿 доступ ко всем сайтам
💳 оплата российскими 🇷🇺 картами 
💰 самая низкая цена на рынке!

⬇️ ⬇️ ⬇️  <i>Жмите кнопку!</i>  ⬇️ ⬇️ ⬇️"""

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("💎 Подключить VPN 💎", callback_data="start_connect")]
        ])

    await message.answer(text, reply_markup=markup)

    async with state.proxy() as data:
        if "msg" in data.keys():
            msg = data["msg"]
            for m in msg:
                try:
                    await bot.delete_message(user_id, m)
                except:
                    pass
            data.pop("msg")


@dp.callback_query_handler(text="start_connect")
async def select_device(call: CallbackQuery):
    text = """<b>🎉 Поздравляем, вы активировали аккаунт <u>IronVPN</u> 

⬇️ ВЫБЕРИТЕ ТАРИФ ⬇️</b>.
    
Lite VPN - это простенький, но мощный VPN, для тех, кто хочет оплачивать 4₽ в день.

далее идет уже IRON VPN, о котором все говорят, это Premium ключи:
 
ЗНАЧОК "🇷🇺" - говорит о том, что это Российский сервер с доступом ко всем * соц.сетям
это лучшие ключи на рынке 😌
"""

    markup = await create_tariffs_markup(call.message.chat.id)

    await call.message.edit_text(text, reply_markup=markup)
