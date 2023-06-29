from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ContentTypes

import states.states
from data.config import ADMINS
from loader import dp, db, bot


@dp.callback_query_handler(text="add_key")
async def get_admin_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("<< назад", callback_data="admin_menu")],
    ])

    await call.message.edit_text("Отправьте файлы VPN.\nВажно! Последовательность: файл .conf + QR код",
                                 reply_markup=markup)

    await states.states.VPN.file.set()


@dp.message_handler(state=states.states.VPN.file, content_types=ContentTypes.DOCUMENT)
@dp.message_handler(state=states.states.VPN.file, content_types=ContentTypes.PHOTO)
async def set_photo(message: types.Message, state: FSMContext):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("⛔️ СТОПЭ", callback_data="admin_menu")]
    ])

    file = False

    async with state.proxy() as data:
        try:
            file = data["file"]
        except:
            data["file"] = message.document.file_id

    if message.photo:
        qr_code = message.photo[-1].file_id

    if file:
        await db.add_vpn(file, qr_code)

        async with state.proxy() as data:
            data.pop("file")

        await message.answer("VPN добавлен!\nОтправьте новый или нажмите кнопку 'СТОПЭ'", reply_markup=markup)

