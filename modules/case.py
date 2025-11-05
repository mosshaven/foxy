from pyrogram import Client, filters
from datetime import datetime, timedelta
from modules.database import db
import random
import re

@Client.on_message(filters.text & filters.regex(r"^(?:[/!.]case|кейс)$", flags=re.I))
async def case_command(client, message):
    user_id = message.from_user.id
    
    # Check case cooldown
    if not await db.can_open_case(user_id):
        user = await db.get_user(user_id)
        if user and user.last_case:
            remaining = (user.last_case + timedelta(hours=24)) - datetime.now()
            hours, remainder = divmod(remaining.seconds, 3600)
            mins, secs = divmod(remainder, 60)
            await message.reply_text(
                f"🤦‍♂️ | Ты уже открывал (-а) кейс недавно...\n"
                f"⏳ | Пиздуй сюда снова через {hours} часов {mins} минут и {secs} секунд"
            )
        return
    
    # Open case
    fb_won = await db.open_case(user_id)
    if fb_won:
        await message.reply_text(f"🧳 | Из кейса тебе выпало {fb_won}💲")
    else:
        await message.reply_text("🤦‍♂️ | Не удалось открыть кейс")
