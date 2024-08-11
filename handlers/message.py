
from aiogram import Router

from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram import Bot

import configparser

import os

config = configparser.ConfigParser()
config.read("settings.ini")
token = config["APIS"]["BOT"]

from handlers.oai import run_oai

from pprint import pprint

message_router = Router()

@message_router.message()
async def message(message: Message, bot: Bot):
    msg = await message.answer("Подготавливаем ответ.")

    if message.content_type == 'text':

        answer = await run_oai(message.text, message.from_user.id)

        await msg.delete()

        if len(answer) > 4095:
            for x in range(0, len(answer), 4095):
                await message.answer(answer[x:x+4095])
        else:
            await message.answer(answer)
        
    elif message.content_type == 'document': ## пока не работает

        if message.caption:
        
            pass
            
        else:
            await msg.edit_text('Укажите ваш запрос!')

    else:
        await msg.edit_text('Формат сообщения не поддерживается.')



