import os
from aiogram import executor
from engine import dp, bot, webh_url

import middles, users, main_loop, admin

import datas
from serv import keep_alive

async def on_startup(_):
    await bot.set_webhook(webh_url)
    # logger = logging.getLogger('peewee')
    # logger.addHandler(logging.StreamHandler())
    # logger.setLevel(logging.DEBUG)

    middles.setup()
    admin.setup()
    users.setup()
    main_loop.setup()
    datas.setup()








if __name__ == "__main__":

    keep_alive()    
    executor.start_webhook(
        dispatcher=dp,
        webhook_path="",
        on_startup=on_startup,
        skip_updates=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
        )

