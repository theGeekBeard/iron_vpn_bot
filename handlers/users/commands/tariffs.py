from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.inline import create_tariffs_markup
from loader import dp


@dp.callback_query_handler(text="tariffs")
@dp.message_handler(commands=["tariffs"])
async def get_tariffs(message: Union[CallbackQuery, Message], state: FSMContext):
    if isinstance(message, CallbackQuery):
        user_id = message.message.chat.id
    else:
        user_id = message.chat.id

    markup = await create_tariffs_markup(user_id)

    text = """<b>⬇️ ВЫБЕРИТЕ ТАРИФ ⬇️</b>.

Lite VPN - это простенький, но мощный VPN, для тех, кто хочет оплачивать 4₽ в день.

далее идет уже IRON VPN, о котором все говорят, это Premium ключи:

ЗНАЧОК "🇷🇺" - говорит о том, что это Российский сервер с доступом ко всем * соц.сетям
это лучшие ключи на рынке 😌
"""

    if isinstance(message, CallbackQuery):
        try:
            await message.message.edit_text(text, reply_markup=markup)
        except:
            message = message.message
            await message.answer(text, reply_markup=markup)

            try:
                await message.delete()
            except:
                pass
    else:
        await message.answer(text, reply_markup=markup)

        try:
            await message.delete()
        except:
            pass
