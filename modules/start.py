from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data import config

@Client.on_message(filters.command("start"))
async def start(client, message):
    user_link = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'
    
    text = f"👋 | Здарова {user_link}. Я развлекательный чат-бот Фокси\n\n"
    text += "Команды:\n"
    text += "/pizza - Сожрать пиццу\n"
    text += "/me - Моя статистика\n"
    text += "/top - Рейтинг лучших пиццаедов\n"
    text += "/case - Открыть кейс (Ежедневно)\n"
    text += "/shop - Магазин\n"
    text += "/dice - Кинуть кубик (При победе 4-10 пицц)\n"
    text += "/casino [ставка] - Крутить рулетку [Х3] (Казино / шанс 11%)\n"
    text += "/pay - Перевести ФБ пользователю\n"
    
    if await is_admin(message.from_user.id):
        text += "/admin - Админ-команды\n"
    
    text += "\nРп команды:\n"
    text += "- Обнять\n"
    text += "- Привет\n"
    text += "- Поцеловать\n"
    text += "- Ударить\n"
    text += "- Трахнуть"
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🧑‍💻 Создатель", url="https://t.me/slutvibe/")],
        [InlineKeyboardButton("🦭 Исходный код", url="https://github.com/mosshaven/foxy")],
        [InlineKeyboardButton(f"🆘 Версия: {config.version}", callback_data="version")]
    ])
    
    await message.reply_text(text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML)

async def is_admin(user_id):
    return user_id in config.admin