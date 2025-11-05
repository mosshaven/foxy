from pyrogram import Client, filters, enums
from modules.database import db
import re

@Client.on_message(filters.text & filters.regex(r"^(?:[/!.](?:me|balance)|б|баланс|мешок)$", flags=re.I))
async def me_command(client, message):
    user_id = message.from_user.id
    
    user = await db.get_user(user_id)
    if not user:
        user = await db.create_user(
            user_id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
    
    # Get display name
    display_name = user.first_name if user.first_name and user.first_name != str(user_id) else message.from_user.first_name
    user_link = f'<a href="tg://user?id={user_id}">{display_name}</a>'
    
    # Calculate pizzeria income (pizzas / 100 = FB per day, just for display)
    pizzeria_income = 0
    if user.pizzas >= 1000:
        pizzeria_income = int(user.pizzas / 100)
    
    response = (
        f"Статистика пользователя {user_link}\n"
        f"Пиццерия: ({pizzeria_income}💲/День)\n"
        f"Количество пицц: {user.pizzas} (🍕)\n"
        f"Количество долларов: {user.foxy_bucks} (💲)\n"
        f"Количество кубиков: {user.cubes} (🎲)\n"
        f"Количество обозлённых школьников: {user.angry_kids} (😡)"
    )
    
    await message.reply_text(response, parse_mode=enums.ParseMode.HTML)
