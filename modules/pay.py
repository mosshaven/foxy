from pyrogram import Client, filters, enums
from modules.database import db
import re

@Client.on_message(filters.text & filters.regex(r"^[/!.]pay\s+(\d+)(?:\s+(\d+))?$", flags=re.I))
async def pay_command(client, message):
    match = re.match(r"^[/!.]pay\s+(\d+)(?:\s+(\d+))?$", message.text, re.I)
    amount = int(match.group(1))
    target_id = None
    
    # Check if user_id provided or reply
    if match.group(2):
        target_id = int(match.group(2))
    elif message.reply_to_message and message.reply_to_message.from_user:
        target_id = message.reply_to_message.from_user.id
    else:
        await message.reply_text("🤦‍♂️ | Укажи пользователя (ответь на сообщение или укажи ID)")
        return
    
    sender_id = message.from_user.id
    
    # Can't pay yourself
    if sender_id == target_id:
        await message.reply_text("🤦‍♂️ | Нельзя переводить самому себе!")
        return
    
    # Can't pay to bot
    bot_me = await client.get_me()
    if target_id == bot_me.id:
        await message.reply_text("🤦‍♂️ | Нельзя переводить боту!")
        return
    
    # Get sender
    sender = await db.get_user(sender_id)
    if not sender or sender.foxy_bucks < amount:
        await message.reply_text(f"🤦‍♂️ | У тебя недостаточно ФБ (нужно {amount}💲)")
        return
    
    # Get or create target
    target = await db.get_user(target_id)
    if not target:
        if message.reply_to_message:
            target_user = message.reply_to_message.from_user
            target = await db.create_user(
                target_id,
                target_user.username,
                target_user.first_name,
                target_user.last_name
            )
        else:
            await message.reply_text("🤦‍♂️ | Пользователь не найден")
            return
    
    # Transfer money
    await db.add_currency(sender_id, foxy_bucks=-amount, angry_kids=1)
    await db.add_currency(target_id, foxy_bucks=amount)
    
    # Get sender display name
    sender_display = message.from_user.first_name
    if sender.first_name and sender.first_name != str(sender_id):
        sender_display = sender.first_name
    
    # Get target display name
    target_display = target.first_name
    if target.first_name == str(target_id):
        # Try to get from message reply
        if message.reply_to_message and message.reply_to_message.from_user:
            target_display = message.reply_to_message.from_user.first_name
        else:
            # Try to get from Telegram
            try:
                tg_user = await client.get_users(target_id)
                target_display = tg_user.first_name
            except:
                target_display = str(target_id)
    
    # Format response
    sender_link = f'<a href="tg://user?id={sender_id}">{sender_display}</a>'
    target_link = f'<a href="tg://user?id={target_id}">{target_display}</a>'
    
    # Get updated sender data
    sender_updated = await db.get_user(sender_id)
    
    response = (
        f"🔃 | {sender_link} перевел (-а) {amount}💲 пользователю {target_link}\n\n"
        f"👀 | За тобой следят {sender_updated.angry_kids} ({sender_updated.angry_kids / 100:.2f}) Школяр (-а/-ов)"
    )
    
    await message.reply_text(response, parse_mode=enums.ParseMode.HTML)
