from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ContentTypes

import states.states
from data.config import ADMINS
from loader import dp, bot


@dp.callback_query_handler(text="admin_menu", state="*")
async def get_admin_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("➕ Добавить ключ", callback_data="add_key")],
        [InlineKeyboardButton("💬 Создать рассылку", callback_data="create_mailing")],
    ])

    await call.message.edit_text("Выберите:", reply_markup=markup)


@dp.message_handler(text="/admin", chat_id=ADMINS)
async def get_admin_menu(message: types.Message, state: FSMContext):
    await state.finish()

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("➕ Добавить ключ", callback_data="add_key")],
        [InlineKeyboardButton("💬 Создать рассылку", callback_data="create_mailing")],
    ])

    await message.answer("Выберите:", reply_markup=markup)
