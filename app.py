import logging
import os

from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
)
from src import *

TELEGRAM_TOKEN = open(f"{ROOT_PATH}/{TELEGRAM_TOKEN_PATH}", 'r').read()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def find_latest_config():
    sorted_files = sorted([f for f in os.listdir(f"{ROOT_PATH}/{HISTORY_PATH}") if f.endswith(".json")], reverse=True)
    if sorted_files != []:
        return sorted_files[0]
    return -1

def main():
    latest_config = find_latest_config()
    config = json.load(open(f"{ROOT_PATH}/{HISTORY_PATH}/{latest_config}", 'r')) if latest_config != -1 else DEFAULT_CONFIG
    bot = Mentai(config=config)
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    for command in ["start"] + list(COMMAND_DICT.keys()):
        command_ = command.replace('/', '')
        handler = CommandHandler(command_, getattr(bot, command_))
        application.add_handler(handler)

    reply_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), bot.reply)
    application.add_handler(reply_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
