import asyncio
from aiogram import Bot, Dispatcher 
from app.components.read_token import read_token
from app.components.working_db import QuizeDatabase
from app.root import router

async def main()-> None:
    TOKEN = await read_token()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    db = QuizeDatabase()
    await db.create_table() 
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__  == '__main__':
    asyncio.run(main())