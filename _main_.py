import asyncio

from aiogram import Dispatcher

from handlers.message import message_router

from handlers.database import Database

db = Database()

from handlers.bot import init_bot

async def main() -> None:


    dp = Dispatcher()

    dp.include_routers(
        message_router
    )
    
    await dp.start_polling(await init_bot())

if __name__ == '__main__':
    asyncio.run(main())

