from pyrogram import Client, filters, enums
from modules.database import db
from modules.cooldown import check_cooldown, get_cooldown_remaining, update_cooldown
import random
import re

@Client.on_message(filters.text & filters.regex(r"^(?:[/!.]dice|кубик)(?:\s+(\d+))?$", flags=re.I))
async def dice_command(client, message):
    user_id = message.from_user.id
    
    # Check global cooldown
    if not await check_cooldown(user_id):
        remaining = await get_cooldown_remaining(user_id)
        await message.reply_text(f"⏳ | Слишком быстро! Попробуй снова через <code>{remaining} секунд</code>", parse_mode=enums.ParseMode.HTML)
        return
    
    match = re.match(r"^(?:[/!.]dice|кубик)(?:\s+(\d+))?$", message.text, re.I)
    count = int(match.group(1) or 1)
    
    user = await db.get_user(user_id)
    
    if not user or user.cubes < count:
        await message.reply_text(f"Еблан блять, у тебя нет столько кубиков ({count}), купи их в магазе")
        return
    
    # Roll dice and calculate pizzas
    total_pizzas = 0
    for _ in range(count):
        roll = random.randint(1, 6)
        if roll >= 4:  # 4, 5, 6 win pizzas
            total_pizzas += random.randint(4, 10)
    
    # Subtract cubes and add pizzas
    await db.add_currency(user_id, cubes=-count, pizzas=total_pizzas)
    await update_cooldown(user_id)
    
    await message.reply_text(
        f"🥳 | Ты кинул (-а) {count} кубиков, с них выпало {total_pizzas} пиццы (🍕)\n"
        f"🎲 | Тебе выпало число: {roll}"
    )
