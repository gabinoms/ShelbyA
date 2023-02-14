from aiogram import executor
from engine import dp, bot
import logging



import middles, users, main_loop, admin

import datas
import asyncio

async def on_startup(_):
    logger = logging.getLogger('peewee')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    middles.setup()
    admin.setup()
    users.setup()
    main_loop.setup()
    datas.setup()








if __name__ == "__main__":
    
    executor.start_polling(dp, skip_updates=True,on_startup=on_startup)


