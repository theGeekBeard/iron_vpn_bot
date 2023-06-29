from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.inline import menuMarkup
from loader import dp, bot, db


@dp.callback_query_handler(text="main_menu", state="*")
async def get_main_menu(call: CallbackQuery, state: FSMContext):
    user_id = call.message.chat.id

    user = await db.get_user(user_id)

    text = f"👤 <b>Ваш ID:</b> <code>{user_id}</code>"

    if user[0]["vpn_id"]:
        term = user[0]["term"]
        text += f"\n⏳ <b>Дней до окончания подписки:</b> <code>{term}</code>\n\n<i>❗️ Если вы потеряли QR код или конфиг файл - вы можете повторно их скачать в разделе 'Мои ключи'.</i>"
    else:
        text += "\n\n🥺 У вас пока нет ключей" \
                "\n\n<i>Выберите нужный вам тариф в разделе 'Тарифы'</i>"

    try:
        await call.message.edit_text(text, reply_markup=menuMarkup)
    except:
        await call.message.answer(text, reply_markup=menuMarkup)

        try:
            await call.message.delete()
        except:
            pass

    async with state.proxy() as data:
        if "msg" in data.keys():
            msg = data["msg"]
            for m in msg:
                try:
                    await bot.delete_message(user_id, m)
                except:
                    pass
            data.pop("msg")
