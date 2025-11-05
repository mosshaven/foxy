import asyncio
import logging
import os

from pyrogram import Client, filters, errors, idle
from pyrogram.handlers import MessageHandler
from data.config import bot_token, api_id, api_hash

async def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting bot")

    for name in (
        "pyrogram",
        "pyrogram.client",
        "pyrogram.session",
        "pyrogram.connection",
        "pyrogram.dispatcher",
    ):
        logging.getLogger(name).setLevel(logging.WARNING)

    plugins_root = "modules"
    discovered_plugins = []
    for dirpath, _, filenames in os.walk(plugins_root):
        for filename in filenames:
            if filename.endswith(".py") and not filename.startswith("_"):
                rel_path = os.path.relpath(os.path.join(dirpath, filename), plugins_root)
                discovered_plugins.append(rel_path.replace(os.sep, "/"))
    if discovered_plugins:
        logging.info("Discovered plugins (%d): %s", len(discovered_plugins), ", ".join(discovered_plugins))
    else:
        logging.info("No plugins found under '%s'", plugins_root)

    app = Client(
        "data/my_account",
        bot_token=bot_token,
        api_id=api_id,
        api_hash=api_hash,
        plugins=dict(root=plugins_root)
    )
    await app.start()
    logging.info("Bot started")

    await idle()

    await app.stop()
    
loop = asyncio.get_event_loop()
loop.run_until_complete(main())