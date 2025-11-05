from pyrogram import Client, filters
from modules.database import db
from data import config
import re

async def is_admin(user_id):
    return user_id in config.admin

@Client.on_message(filters.text & filters.regex(r"^/give\s+(\d+)\s+(\d+)$"))
async def give_fb(client, message):
    if not await is_admin(message.from_user.id):
        return
    
    target_id = int(message.matches[0].group(1))
    amount = int(message.matches[0].group(2))
    
    # Ensure user exists
    user = await db.get_user(target_id)
    if not user:
        await db.create_user(target_id, None, str(target_id), None)
    
    await db.add_currency(target_id, foxy_bucks=amount)
    await message.reply_text(f"💰 | Выдано {amount}💲 пользователю {target_id}")

@Client.on_message(filters.text & filters.regex(r"^/give_pizzas\s+(\d+)\s+(\d+)$"))
async def give_pizzas(client, message):
    if not await is_admin(message.from_user.id):
        return
    
    target_id = int(message.matches[0].group(1))
    amount = int(message.matches[0].group(2))
    
    # Ensure user exists
    user = await db.get_user(target_id)
    if not user:
        await db.create_user(target_id, None, str(target_id), None)
    
    await db.add_currency(target_id, pizzas=amount)
    await message.reply_text(f"🍕 | Выдано {amount} пицц пользователю {target_id}")

@Client.on_message(filters.text & filters.regex(r"^/give_cubes\s+(\d+)\s+(\d+)$"))
async def give_cubes(client, message):
    if not await is_admin(message.from_user.id):
        return
    
    target_id = int(message.matches[0].group(1))
    amount = int(message.matches[0].group(2))
    
    # Ensure user exists
    user = await db.get_user(target_id)
    if not user:
        await db.create_user(target_id, None, str(target_id), None)
    
    await db.add_currency(target_id, cubes=amount)
    await message.reply_text(f"🎲 | Выдано {amount} кубиков пользователю {target_id}")

@Client.on_message(filters.text & filters.regex(r"^/reset_cd\s+(\d+)$"))
async def reset_cooldowns(client, message):
    if not await is_admin(message.from_user.id):
        return
    
    target_id = int(message.matches[0].group(1))
    
    # Reset all cooldowns
    async with db.async_session() as session:
        from modules.database import User
        user = await session.get(User, target_id)
        if user:
            user.last_pizza = None
            user.last_case = None
            user.last_pizzeria = None
            await session.commit()
            await message.reply_text(f"🔄 | Сброшены все кулдауны для пользователя {target_id}")
        else:
            await message.reply_text(f"🤷‍♂️ | Пользователь {target_id} не найден")

@Client.on_message(filters.text & filters.regex(r"^/admin$", flags=re.I))
async def admin_help(client, message):
    if not await is_admin(message.from_user.id):
        return
    
    help_text = """
👑 Админ-команды:

/give [id] [amount] - Выдать ФБ
/give_pizzas [id] [amount] - Выдать пиццы
/give_cubes [id] [amount] - Выдать кубики
/reset_cd [id] - Сбросить все кулдауны пользователя
"""
    await message.reply_text(help_text)
