from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, MediaGroup, InputMedia, \
    InputMediaPhoto, InputMediaDocument

from data.callback_data import vpns_cd, qr_code_cd
from loader import dp, db, bot


@dp.message_handler(commands=["my_key"])
@dp.callback_query_handler(text="my_keys")
async def my_key(message: Union[types.Message, CallbackQuery], state: FSMContext):
    callback = False
    if isinstance(message, CallbackQuery):
        callback = True

    if callback:
        user_id = message.message.chat.id
    else:
        user_id = message.chat.id

    user = await db.get_user(user_id)

    vpn_id1 = user[0]["vpn_id"]
    vpn_id2 = user[0]["vpn_id2"]

    if callback:
        message = message.message

    if not vpn_id1:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")],
        ])
        text = "🥺 У вас пока нет ключей" \
               "\n\n<i>Выберите нужный вам тариф в разделе 'Тарифы'</i>"
        await message.answer(text, reply_markup=markup)

        try:
            await message.delete()
        except:
            pass
    else:

        if vpn_id2:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton("🔑 Ключ 1", callback_data=vpns_cd.new(vpn_id=vpn_id1)),
                 InlineKeyboardButton("🔑 Ключ 2", callback_data=vpns_cd.new(vpn_id=vpn_id2))],
                [InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")],
            ])
        else:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton("🏞 QR код", callback_data=qr_code_cd.new(vpn_id=vpn_id1))],
                [InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")],
            ])

        text = """🔑 <b>Ваши ключи</b>"""

        vpn = await db.get_vpn(vpn_id1)
        file = vpn[0]["file_id"]

        media = InputMediaDocument(file, caption=text)

        if not vpn_id2:
            try:
                await message.edit_media(media, reply_markup=markup)
            except:
                await message.answer_document(file, caption=text, reply_markup=markup)

                try:
                    await message.delete()
                except:
                    pass
        else:
            try:
                await message.edit_text(text, reply_markup=markup)
            except:
                await message.answer(text, reply_markup=markup)

                try:
                    await message.delete()
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


@dp.callback_query_handler(vpns_cd.filter())
async def get_vpn(call: CallbackQuery, state: FSMContext, callback_data: dict = None):
    if callback_data:
        vpn_id = int(callback_data["vpn_id"])
        async with state.proxy() as data:
            data["vpn_id"] = vpn_id
    else:
        async with state.proxy() as data:
            vpn_id = data["vpn_id"]

    vpn = await db.get_vpn(vpn_id)
    file = vpn[0]["file_id"]

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("🏞 QR код", callback_data=qr_code_cd.new(vpn_id=vpn_id))],
        [InlineKeyboardButton("⬅️ Назад", callback_data="my_keys")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ])

    text = """🔑 <b>Ваш ключ</b>"""

    media = InputMediaDocument(file, caption=text)

    try:
        await call.message.edit_media(media, reply_markup=markup)
    except:
        await call.message.answer_document(file, caption=text, reply_markup=markup)
        try:
            await call.message.delete()
        except:
            pass


@dp.callback_query_handler(qr_code_cd.filter())
async def get_qr_code(call: CallbackQuery, callback_data: dict):
    vpn_id = int(callback_data["vpn_id"])

    vpn = await db.get_vpn(vpn_id)
    qr_code = vpn[0]["photo_id"]

    text = """🏞 <b>Ваш QR код</b>"""

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("⬅️ Назад", callback_data="my_keys")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ])

    media = InputMediaPhoto(qr_code, caption=text)

    await call.message.edit_media(media, reply_markup=markup)
