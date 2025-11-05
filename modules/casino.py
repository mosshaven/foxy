from pyrogram import Client, filters, enums
from modules.database import db
from modules.cooldown import check_cooldown, get_cooldown_remaining, update_cooldown
import random
import re

@Client.on_message(filters.text & filters.regex(r"^(?:[/!.]casino|казино)(?:\s+(\d+))?$", flags=re.I))
async def casino_command(client, message):
    user_id = message.from_user.id
    
    # Check global cooldown
    if not await check_cooldown(user_id):
        remaining = await get_cooldown_remaining(user_id)
        await message.reply_text(f"⏳ | Слишком быстро! Попробуй снова через <code>{remaining} секунд</code>", parse_mode=enums.ParseMode.HTML)
        return
    
    # Parse bet amount
    match = re.match(r"^(?:[/!.]casino|казино)(?:\s+(\d+))?$", message.text, re.I)
    bet = int(match.group(1) or 100)
    
    if bet < 100:
        await message.reply_text("🤦‍♂️ | Минимальная ставка 100💲")
        return
    
    user = await db.get_user(user_id)
    if not user or user.foxy_bucks < bet:
        await message.reply_text(f"🤦‍♂️ | У тебя недостаточно ФБ для игры в казино (нужно {bet}💲)")
        return
    
    # 11% chance to win
    win = random.randint(1, 100) <= 11
    
    if win:
        winnings = bet * 3  # x3
        profit = bet * 2  # Net profit
        await db.add_currency(user_id, foxy_bucks=profit)
        await message.reply_text(
            f"🎰 | Ты выиграл в казино!\n"
            f"💰 | Получено: {winnings}💲 (x3)"
        )
    else:
        await db.add_currency(user_id, foxy_bucks=-bet)
        await message.reply_text(
            f"🎰 | Ты проиграл в казино!\n"
            f"💸 | Потеряно: {bet}💲"
        )
    
    await update_cooldown(user_id)
