from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ContentTypes

import states.states
from data.config import ADMINS
from loader import dp, db, bot


@dp.callback_query_handler(text="create_mailing")
async def get_admin_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("<< назад", callback_data="admin_menu")],
    ])

    await call.message.edit_text("Отправьте картинку или текст:", reply_markup=markup)

    await states.states.Mail.text.set()


@dp.message_handler(state=states.states.Mail.text, content_types=ContentTypes.PHOTO)
@dp.message_handler(state=states.states.Mail.text)
async def set_mail_text(message: types.Message, state: FSMContext):
    await state.finish()

    users = await db.get_users()

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("<< назад", callback_data="admin_menu")],
    ])

    await message.answer("Рассылка отправлена!", reply_markup=markup)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("✅ прочитано", callback_data="ok")],
    ])

    if message.photo:
        photo = message.photo[-1].file_id
        caption = message.caption

        for user in users:
            try:
                await bot.send_photo(user["user_id"], photo, caption=caption, caption_entities=message.caption_entities, reply_markup=markup)
            except:
                continue
    else:
        text = message.html_text

        for user in users:
            try:
                await bot.send_message(user["user_id"], text, parse_mode="HTML", reply_markup=markup)
            except:
                continue