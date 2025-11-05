import asyncio
import logging
import os
from logging.handlers import RotatingFileHandler
from modules.database import db

from pyrogram import Client, filters, errors, idle
from pyrogram.handlers import MessageHandler
from data.config import bot_token, api_id, api_hash

async def main():
    os.makedirs("data", exist_ok=True)
    
    # Clear old logs
    for log_file in ['data/logs.log', 'data/errors.log']:
        if os.path.exists(log_file):
            open(log_file, 'w').close()
    
    # Setup logging
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Main logs (INFO only, no errors)
    main_handler = RotatingFileHandler('data/logs.log', maxBytes=5*1024*1024, backupCount=3)
    main_handler.setFormatter(log_formatter)
    main_handler.setLevel(logging.INFO)
    main_handler.addFilter(lambda record: record.levelno < logging.ERROR)
    
    # Error logs (ERROR and above only)
    error_handler = RotatingFileHandler('data/errors.log', maxBytes=5*1024*1024, backupCount=3)
    error_handler.setFormatter(log_formatter)
    error_handler.setLevel(logging.ERROR)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(main_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(console_handler)
    
    logging.info("Starting bot")

    for name in (
        "pyrogram",
        "pyrogram.client",
        "pyrogram.session",
        "pyrogram.connection",
        "pyrogram.dispatcher",
    ):
        logging.getLogger(name).setLevel(logging.WARNING)

    await db.init_db()

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