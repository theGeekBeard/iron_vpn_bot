import asyncio
import datetime

import pytz
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import ADMINS
from loader import db, bot

markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("✅ прочитано", callback_data="ok")],
])


async def mail(user_id, text):
    try:
        await bot.send_message(user_id, text, reply_markup=markup)
    except:
        pass


async def mail_to_admin(text, user_id=None):
    for admin in ADMINS:
        if user_id:
            user = await db.get_user(user_id)
            vpn_id = user[0]["vpn_id"]
            vpn = await db.get_vpn(vpn_id)
            file = vpn[0]["file_id"]
            await bot.send_document(admin, file, caption=text)
        else:
            await bot.send_message(admin, text)


async def check_subscribe():
    while True:
        if datetime.datetime.now(pytz.timezone('Europe/Moscow')).hour == 12 and datetime.datetime.now(
                pytz.timezone('Europe/Moscow')).minute == 52:
            users = await db.get_users()
            print(1)
            for user in users:
                if not user["term"] is None:
                    print(9999999999999999)
                    if user["vpn_id"]:
                        user_id = user["user_id"]
                        username = user["username"]
                        full_name = user["full_name"]
                        term = user["term"]
                        print(term)
                        if term <= 0:
                            text = """🥺 <b>Ваш срок тарифа истек. Ключи удалены и будут заблокированы.</b>\n\n❗️ <i>после приобретение нового тарифа, 
не забудьте установить ключ который вам пришлет бот</i>"""

                            text_for_admin = f"""❗️ Истечение срока подписки ❗️
ID: {user_id}                  
Username: @{username}
 Имя пользователя: {full_name}
        
✏️ Нужно заблокировать ключ"""

                            await mail(user_id, text)
                            await mail_to_admin(text_for_admin, user_id)

                            await db.update_user_info(user_id, {"paid": False, "vpn_id": None})
                            continue
            else:
                await asyncio.sleep(60)
        else:
            await asyncio.sleep(60)


async def rebalanced_users():
    while True:
        if datetime.datetime.now(pytz.timezone('Europe/Moscow')).hour == 12 and datetime.datetime.now(
                pytz.timezone('Europe/Moscow')).minute == 40:
            users = await db.get_users()

            for user in users:
                if user["vpn_id"]:
                    user_id = user["user_id"]
                    term = user["term"]
                    if term:
                        if term > 0:
                            await db.update_user_info(user_id, {"term": term - 1})
            else:
                await asyncio.sleep(60)
        else:
            await asyncio.sleep(60)
