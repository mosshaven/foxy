from pyrogram import Client, filters, enums
from modules.database import db
import json
import re

RANKS = {
    1: "🥇",
    2: "🥈",
    3: "🥉",
}

@Client.on_message(filters.text & filters.regex(r"^(?:[/!.]top|топ)$", flags=re.I))
async def top_command(client, message):
    status_msg = await message.reply_text("Чекаю жиробасов...")
    await db.save_top_pizza()
    
    try:
        with open('data/top.json') as f:
            top = json.load(f)
    except:
        await status_msg.edit_text("🤷‍♂️ | Топ пока пустой")
        return
    
    if not top:
        await status_msg.edit_text("🤷‍♂️ | Топ пока пустой")
        return
    
    response = "🏆 Рейтинг жирдяев вселенной\n\n"
    
    for i, entry in enumerate(top[:25], 1):
        rank_emoji = RANKS.get(i, "🍃")
        # Get full name from database
        user = await db.get_user(entry["id"])
        if user and user.first_name and user.first_name != str(entry["id"]):
            full_name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
        else:
            # Try to get from Telegram
            try:
                tg_user = await client.get_users(entry["id"])
                full_name = f"{tg_user.first_name} {tg_user.last_name}" if tg_user.last_name else tg_user.first_name
            except:
                full_name = entry["username"] or str(entry["id"])
        user_link = f'<a href="tg://user?id={entry["id"]}">{full_name}</a>'
        response += f"[{i}|{rank_emoji}] {user_link}: {entry['pizzas']}\n"
    
    await status_msg.edit_text(response, parse_mode=enums.ParseMode.HTML)
