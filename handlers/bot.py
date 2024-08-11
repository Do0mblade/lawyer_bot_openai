

from aiogram import Bot

import configparser

async def init_bot():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    bot = Bot(config["APIS"]["BOT"])
    return bot

