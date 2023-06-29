from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "🏠 Главное меню"),
            types.BotCommand("my_key", "🔑 Мой ключ"),
            types.BotCommand("tariffs", "📋 Тарифы"),
            types.BotCommand("help", "🆘 Помощь")
        ]
    )
