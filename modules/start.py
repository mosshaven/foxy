from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import command_prefixes, version

@Client.on_message(filters.command("start", prefixes=command_prefixes))
async def start_handler(client, message):
    await client.send_message(
        chat_id=message.chat.id,
        text=(
            f"Привет, <a href=\"tg://user?id={message.from_user.id}\">{message.from_user.first_name}</a>! "
            f"Я Фоксян, развлекательный чат-бот."
        ),
        parse_mode=enums.ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("🧑‍💻 | Создатель", url='https://t.me/slutvibe')],
                [InlineKeyboardButton("📤 | Исходный код бота", url='https://github.com/mosshaven/foxy')],
                [InlineKeyboardButton(f"🆘 | Версия бота: {version}", callback_data="noop_version")]
            ]
        )
    )

@Client.on_callback_query()
async def on_callback_noop(client, callback_query):
    if callback_query.data == "noop_version":
        await callback_query.answer()