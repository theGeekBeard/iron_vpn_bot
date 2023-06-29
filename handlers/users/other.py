from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentTypes

from loader import dp


@dp.callback_query_handler(text="ok", state="*")
async def ok(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.delete()

#
# @dp.message_handler(content_types=ContentTypes.STICKER)
# async def del_messages(message: types.Message):
#     print(message.sticker.file_id)
#
#
# @dp.message_handler(content_types=ContentTypes.PHOTO)
# async def photo(message: types.Message):
#     print(message.photo[-1].file_id)
#
#
# @dp.message_handler(content_types=ContentTypes.VIDEO)
# async def photo(message: types.Message):
#     print(message.video.file_id)


@dp.message_handler(content_types=ContentTypes.ANY)
async def del_messages(message: types.Message):
    await message.delete()
