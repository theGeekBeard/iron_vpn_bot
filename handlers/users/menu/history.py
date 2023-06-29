from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.inline import menuMarkup
from loader import dp, db, bot


@dp.callback_query_handler(text="history")
async def get_my_devices(call: CallbackQuery, state: FSMContext):
    payment_history = await db.get_payment_history(call.message.chat.id)

    text = """<pre>ДАТА, ВРЕМЯ          ₽  ТИП</pre>\n"""

    for payment in payment_history:
        text += f'<pre>{payment["datetime"].replace("T", " ")[:16]}' \
                f'     {payment["amount"]}  {payment["type"]}\n</pre>'

    markup = InlineKeyboardMarkup(inline_keyboard=[
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
