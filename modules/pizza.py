from pyrogram import Client, filters, enums
from datetime import datetime, timedelta
from modules.database import db
from modules.cooldown import check_cooldown, get_cooldown_remaining, update_cooldown
import random
import re

@Client.on_message(filters.text & filters.regex(r"^(?:[/!.]pizza|пицца)$", flags=re.I))
async def pizza_command(client, message):
    user_id = message.from_user.id
    
    # Check global cooldown
    if not await check_cooldown(user_id):
        remaining = await get_cooldown_remaining(user_id)
        await message.reply_text(f"⏳ | Слишком быстро! Попробуй снова через <code>{remaining} секунд</code>", parse_mode=enums.ParseMode.HTML)
        return
    
    # Get or create user
    user = await db.get_user(user_id)
    if not user:
        user = await db.create_user(
            user_id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
    
    # Check pizza cooldown
    if not await db.can_eat_pizza(user_id):
        if user.last_pizza:
            remaining = (user.last_pizza + timedelta(minutes=15)) - datetime.now()
            mins, secs = divmod(remaining.seconds, 60)
            await message.reply_text(
                f"🤦‍♂️ | Ты уже жрал (-а) недавно пиццу...\n"
                f"⏳ | Пиздуй сюда снова через {mins} минут и {secs} секунд"
            )
            await update_cooldown(user_id)
        return
    
    # Eat pizza and calculate FB reward
    await db.eat_pizza(user_id)
    
    # Refresh user data
    user = await db.get_user(user_id)
    
    # Calculate pizzeria income (1000+ pizzas)
    fb_earned = 0
    if user.pizzas >= 1000:
        fb_earned = random.randint(30, 70)
        await db.add_currency(user_id, foxy_bucks=fb_earned)
    
    # Response message
    response = (
        f"🤤 | Ты схавал (-а) кусок пиццы (🍕)\n"
        f"🏦 | В твоём желудке: {user.pizzas} кусков пиццы"
    )
    
    await update_cooldown(user_id)
    await message.reply_text(response)
    
    # Check pizzeria income (once per day)
    if await db.can_claim_pizzeria(user_id):
        income = await db.claim_pizzeria(user_id)
        if income:
            await message.reply_text(
                f"💰 | Ваша пиццерия принесла вам {income}💲\n"
                f"🥳 | Так держать!"
            )
