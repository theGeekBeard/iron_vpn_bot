import asyncio

from aiogram import executor
from aiogram.types import PreCheckoutQuery

import handlers

from loader import dp, bot
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.shedulers import check_subscribe, rebalanced_users


async def on_startup(dispatcher):
    # проверка подписки
    asyncio.create_task(check_subscribe())

    # ребаланс пользователей
    asyncio.create_task(rebalanced_users())

    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
