from pyrogram import Client, filters, enums
from modules.database import db
import re

SHOP_ITEMS = {
    "🍕": {"price": 30, "reward": {"pizzas": 1}},
    "пицца": {"price": 30, "reward": {"pizzas": 1}},
    "pizza": {"price": 30, "reward": {"pizzas": 1}},
    "🎲": {"price": 15, "reward": {"cubes": 1}},
    "кубик": {"price": 15, "reward": {"cubes": 1}},
    "cube": {"price": 15, "reward": {"cubes": 1}},
}

@Client.on_message(filters.text & filters.regex(r"^(?:[/!.]shop|магазин|магаз)$", flags=re.I))
async def shop_list(client, message):
    text = (
        "Приветствую тебя в магазе!\n"
        "За Фокси-баксы:\n"
        "30💲 = 1<code>🍕</code>\n"
        "15💲 = 1<code>🎲</code>\n"
        "Для покупки пиши: /shop [Предмет] [Количество]\n"
        "Пример: /shop 🍕 1"
    )
    await message.reply_text(text, parse_mode=enums.ParseMode.HTML)

@Client.on_message(filters.text & filters.regex(r"^(?:[/!.]shop|(?:[/!.]buy|купить))\s+(.+?)\s+(\d+)$", flags=re.I))
async def shop_buy(client, message):
    match = re.match(r"^(?:[/!.]shop|(?:[/!.]buy|купить))\s+(.+?)\s+(\d+)$", message.text, re.I)
    item_name = match.group(1).lower().strip()
    count = int(match.group(2))
    
    if count <= 0 or count > 100:
        await message.reply_text("🤦‍♂️ | Количество должно быть от 1 до 100")
        return
    
    if item_name not in SHOP_ITEMS:
        await message.reply_text("🤷‍♂️ | Такого товара нет в магазине")
        return
    
    item = SHOP_ITEMS[item_name]
    total_price = item["price"] * count
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user or user.foxy_bucks < total_price:
        await message.reply_text(f"🤦‍♂️ | У тебя недостаточно ФБ (нужно {total_price}💲)")
        return
    
    # Process purchase
    reward_key = list(item["reward"].keys())[0]
    reward_value = list(item["reward"].values())[0] * count
    
    await db.add_currency(
        user_id,
        foxy_bucks=-total_price,
        **{reward_key: reward_value}
    )
    
    emoji = "🍕" if reward_key == "pizzas" else "🎲"
    await message.reply_text(
        f"🛍 | Ты купил (-а) {count}x {emoji} за {total_price}💲"
    )
