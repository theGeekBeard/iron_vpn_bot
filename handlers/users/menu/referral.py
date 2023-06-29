from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from data.config import BOT_NICKNAME
from keyboards.inline.inline import menuMarkup
from loader import dp, db, bot


@dp.callback_query_handler(text="referral")
async def get_my_devices(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id
    user = await db.get_user(user_id)

    text = f"""📌 <b>Ваша реферальная ссылка:</b> <code>https://t.me/{BOT_NICKNAME}?start={user_id}</code>

💰 <b>Баланс:</b> {user[0]['balance']}₽
👥 <b>Кол-во рефералов:</b> {user[0]['ref_count']}

<i>❗️ За каждого приведенного пользователя Вам на баланс будет начисляться 15% от общей суммы его покупки</i>"""

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("🔑 Купить ключ за баланс", callback_data="buy_key_balance")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")]
    ])

    try:
        await call.message.edit_text(text, reply_markup=markup)
    except:
        await call.message.answer(text, reply_markup=markup)
        try:
            await call.message.delete()
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
