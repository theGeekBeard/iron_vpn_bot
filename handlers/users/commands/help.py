from typing import Union

from aiogram import types
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from data.callback_data import help_cd
from data.config import ADMINS, VIDEOS
from loader import dp, db, bot


@dp.message_handler(commands=["help"])
@dp.callback_query_handler(text="help")
async def get_my_devices(message: Union[CallbackQuery, types.Message]):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("VPN — НЕ РАБОТАЕТ", callback_data="help_1")],
        [InlineKeyboardButton("НИЗКАЯ СКОРОСТЬ", callback_data="help_2")],
        [InlineKeyboardButton("ОТПРАВИТЬ МОЙ КЛЮЧ НА ПРОВЕРКУ", callback_data="help_3")],
        [InlineKeyboardButton("ИНСТ. ПЛОХО ГРУЗИТ", callback_data="help_4")],
        [InlineKeyboardButton("📱 Android", callback_data=help_cd.new(device="android")),
         InlineKeyboardButton("📱 iOS(iPhone, iPad)", callback_data=help_cd.new(device="iphone"))],
        [InlineKeyboardButton("Написать в поддержку 💬", url="https://t.me/iron_vpn_support")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ])

    text = """<b>Что вас интересует?</b>"""

    if isinstance(message, CallbackQuery):
        try:
            await message.message.edit_text(text, reply_markup=markup)
        except:
            await message.message.answer(text, reply_markup=markup)

            try:
                await message.message.delete()
            except:
                pass
    else:
        await message.answer(text, reply_markup=markup)

        try:
            await message.delete()
        except:
            pass


@dp.callback_query_handler(text="help_4")
async def help_1(call: CallbackQuery):
    text = """— дело в приложении *инст. 

как решить проблему? 
нужно удалить и заново установить приложение *инст. 

— обязательно перед этим, убедитесь в том, что вы знаете свой пароль."""

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("⬅️ Назад", callback_data="help")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ])

    await call.message.edit_text(text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=markup)


@dp.callback_query_handler(text="help_1")
async def help_1(call: CallbackQuery):
    text = """— иногда, в очень редких случаях, кэш забивается и нужно сделать следующее: 
<b>ПЕРЕЗАГРУЗИТЬ ТЕЛЕФОН</b>

а так же: 

— проверьте пожалуйста, у вас точно установлен тот ключ, который вы получили после оплаты ? 
посмотреть свой ключ можно нажав 
/my_key

— если вы все проверили, но впн не работает, <a href="https://t.me/iron_vpn_support">напишите нам</a> 💬"""

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("⬅️ Назад", callback_data="help")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ])

    await call.message.edit_text(text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=markup)


@dp.callback_query_handler(text="help_2")
async def help_2(call: CallbackQuery):
    text = """— Мы не допускаем перегрузки наших серверов, и невысокая скорость почти всегда означает проблемы местных или транзитных провайдеров. Нагрузки растут, а новые каналы связи в Европу в условиях санкций не строятся. Нагрузка также зависит от времени суток.

В крайнем случае, см. пункт впн <b>не работает.</b>"""

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("⬅️ Назад", callback_data="help")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ])

    await call.message.edit_text(text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=markup)


@dp.callback_query_handler(text="help_3")
async def help_3(call: CallbackQuery):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("📤 Отправить ключ", callback_data="send_key")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="help")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ])

    await call.message.edit_text("Отправить ключ на проверку?", parse_mode="HTML", disable_web_page_preview=True,
                                 reply_markup=markup)


@dp.callback_query_handler(text="send_key")
async def send_key(call: CallbackQuery):
    text = """— ваш ключ был отправлен на проверку

дождитесь отчета по вашему ключу. 
с вами свяжется тех.поддержка 
IRON VPN.
по результатам проверки вам могут прислать новый ключ 🔑 либо перезагрузить сервер на котором он был выпущен. 

спасибо за обращение 🫶🏻"""

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("⬅️ Назад", callback_data="help")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ])

    await call.message.edit_text(text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=markup)

    user = await db.get_user(call.message.chat.id)

    for admin in ADMINS:
        vpn_id = user[0]["vpn_id"]
        if vpn_id:
            vpn = await db.get_vpn(vpn_id)
            file_id = vpn[0]["file_id"]

            await bot.send_document(admin, file_id,
                                    caption=f"⚙️ Запрос на проверку ⚙️\n\nПользователь: @{call.message.chat.username} - {call.message.chat.full_name}"
                                            f"\nID ключа: {user[0]['vpn_id']}")


@dp.callback_query_handler(help_cd.filter())
async def get_help(call: CallbackQuery, callback_data: dict):
    device = callback_data["device"]

    video = VIDEOS[device]
    if device == "android":
        text = """• Установите приложение IRON VPN ❤️ <a href="https://play.google.com/store/apps/details?id=com.wireguardironvpn.android&hl=ru&gl=US">нажмите сюда, чтобы установить</a>
• Нажмите на три точки рядом с ключом (выше в чате hit_*.conf)
и сохраните его в "Загрузки"
• Запустите программу IRON VPN
   нажмите ➕ внизу экрана справа
• Нажмите кнопку “Импорт из файла или архива”, выберите скачанный ключ из папки загрузок
• Включите тумблер.

также вы можете переслать QR код на другое устройство и отсканировать его из программы IRON VPN, 
нажав ➕. Введите имя туннеля: iron

один и тот же QR код и ключ файл можно использовать только на одном устройстве!"""
    else:
        text = """• Установите приложение WireGuard <a href="https://apps.apple.com/ru/app/wireguard/id1441195209">нажмите сюда, чтобы установить</a>
• Нажмите на ключ (выше в чате hit_*.conf)
• В углу нажмите стрелку "Поделиться"
• В списке программ выберите WireGuard
• Включите тумблер

также вы можете переслать QR код на другое устройство и отсканировать его из программы WireGuard, 
нажав ➕. Введите имя туннеля: iron

Oдин и тот же QR код и конфиг файл можно использовать только на одном устройстве!"""

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("⬅️ Назад", callback_data="help")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")],
    ])

    await call.message.answer_video(video, caption=text, reply_markup=markup)

    try:
        await call.message.delete()
    except:
        pass
