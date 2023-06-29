from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from data.callback_data import agree_cd
from loader import dp


@dp.callback_query_handler(text="rules")
async def get_my_devices(call: CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Политика конфеденциальности", callback_data=agree_cd.new(num=1))],
        [InlineKeyboardButton("Пользовательское соглашение", callback_data=agree_cd.new(num=2))],
        [InlineKeyboardButton("Оплата и возврат", callback_data=agree_cd.new(num=3))],
        [InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")],
    ])

    try:
        await call.message.edit_text("📋 Оферта", reply_markup=markup)
    except:
        await call.message.answer("📋 Оферта", reply_markup=markup)
        try:
            await call.message.delete()
        except:
            pass


@dp.callback_query_handler(agree_cd.filter())
async def get_agree_document(call: CallbackQuery, callback_data: dict):
    num = int(callback_data["num"])

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("⬅️ Назад", callback_data="rules")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ])

    if num == 1:
        document = "BQACAgIAAxkBAAED3XJkAjfL2heDLKpANkO66zTifcApfAACHyQAAubtGUjNC_J4hcfeXS4E"
    elif num == 2:
        document = "BQACAgIAAxkBAAEDgDNj_5gYd7zlTWMfDJws60JDyZJXHwACUCgAAnt-qEs9LHEnZciuMy4E"
    else:
        document = "BQACAgIAAxkBAAEDgDlj_5hQmdsAATmL4qsH1Ni75LEBAWIAAk8wAAKWbfhLDWjiA9CYRq4uBA"

    await call.message.answer(document, reply_markup=markup)
    await call.message.delete()
