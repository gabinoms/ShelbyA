from engine import scheduler
from config import ADMIN

async def run(message):
    if str(message.chat.id) in ADMIN:        
        scheduler.start()
        await message.answer('scheduler starts...')
    else:
        await message.delete()


async def pause(message):
    if str(message.chat.id) in ADMIN:        
        scheduler.pause()
        await message.answer('scheduler paused...')
    else:
        await message.delete()


async def resume(message):
    if str(message.chat.id) in ADMIN:        
        scheduler.resume()
        await message.answer('scheduler resumed...')
    else:
        await message.delete()


async def stop(message):
    if str(message.chat.id) in ADMIN:        
        scheduler.shutdown()
        await message.answer('stopped...')
    else:
        await message.delete()