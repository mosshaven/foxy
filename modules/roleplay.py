from pyrogram import Client, filters, enums
import re
import random


async def process_roleplay(client, message, media_url, verb, past_verb):
    sender = message.from_user
    sender_display = (
        f"{sender.first_name} {sender.last_name}" if sender.last_name else sender.first_name
    )
    sender_link = f'<a href="tg://user?id={sender.id}">{sender_display}</a>'

    if message.reply_to_message and message.reply_to_message.from_user:
        target_user = message.reply_to_message.from_user
    else:
        target_user = await client.get_me()

    target_display = (
        f"{target_user.first_name} {target_user.last_name}" if target_user.last_name else target_user.first_name
    )
    target_link = f'<a href="tg://user?id={target_user.id}">{target_display}</a>'

    match = re.match(r"^(?:/\w+|[а-яё]+)(?:\s+(.*))?$", message.text, re.I)
    extra_text = match.group(1) if match and match.group(1) else None

    text = (
        f'<a href="{media_url}">🤗</a> | '
        f'{sender_link} '
        f'{past_verb} {target_link}'
    )
    
    if extra_text:
        text += f'\nСо словами: <code>{extra_text}</code>'

    await message.reply_text(text, parse_mode=enums.ParseMode.HTML)


@Client.on_message(filters.text & filters.regex(r"^обнять(?:\s+(.*))?$", flags=re.I))
async def hug(client, message):
    rnd = random.randint(1, 9)
    media_url = f"https://raw.githubusercontent.com/a9-fm/a9-fm.github.io/master/Foxy/hug/{rnd}.mp4"

    sender = message.from_user
    sender_display = (
        f"{sender.first_name} {sender.last_name}" if sender.last_name else sender.first_name
    )
    sender_link = f'<a href="tg://user?id={sender.id}">{sender_display}</a>'

    if message.reply_to_message and message.reply_to_message.from_user:
        target_user = message.reply_to_message.from_user
    else:
        target_user = await client.get_me()

    target_display = (
        f"{target_user.first_name} {target_user.last_name}" if target_user.last_name else target_user.first_name
    )
    target_link = f'<a href="tg://user?id={target_user.id}">{target_display}</a>'

    match = re.match(r"^обнять(?:\s+(.*))?$", message.text, re.I)
    extra_text = match.group(1) if match and match.group(1) else None

    text = (
        f'<a href="{media_url}">🤗</a> | '
        f'{sender_link} '
        f'Обнял (-а) {target_link}'
    )
    
    if extra_text:
        text += f'\nСо словами: <code>{extra_text}</code>'

    await message.reply_text(text, parse_mode=enums.ParseMode.HTML)


@Client.on_message(filters.text & filters.regex(r"^(?:ударить|уебать)(?:\s+(.*))?$", flags=re.I))
async def hit(client, message):
    rnd = random.randint(1, 9)
    media_url = f"https://raw.githubusercontent.com/a9-fm/a9-fm.github.io/master/Foxy/damage/{rnd}.mp4"
    await process_roleplay(client, message, media_url, "ударить", "Ударил (-а)")


@Client.on_message(filters.text & filters.regex(r"^(?:привет|приветик)(?:\s+(.*))?$", flags=re.I))
async def greet(client, message):
    rnd = random.randint(1, 9)
    media_url = f"https://raw.githubusercontent.com/a9-fm/a9-fm.github.io/master/Foxy/hello/{rnd}.mp4"
    await process_roleplay(client, message, media_url, "привет", "Поприветствовал (-а)")


@Client.on_message(filters.text & filters.regex(r"^поцеловать(?:\s+(.*))?$", flags=re.I))
async def kiss(client, message):
    rnd = random.randint(1, 9)
    media_url = f"https://raw.githubusercontent.com/a9-fm/a9-fm.github.io/master/Foxy/kiss/{rnd}.mp4"
    await process_roleplay(client, message, media_url, "поцеловать", "Поцеловал (-а)")


@Client.on_message(filters.text & filters.regex(r"^(?:трахнуть|выебать|оттрахать)(?:\s+(.*))?$", flags=re.I))
async def sex(client, message):
    rnd = random.randint(1, 9)
    media_url = f"https://raw.githubusercontent.com/a9-fm/a9-fm.github.io/master/Foxy/sex/{rnd}.mp4"
    await process_roleplay(client, message, media_url, "трахнуть", "Трахнул (-а)")