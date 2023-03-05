
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram import types

from datas.bh_methods import check_jumper, get_silent, get_silent_word_count
from main_loop.ada_moves import letsplay

from engine import bot
from config import CHAT, ADMIN


class BetMiddle(BaseMiddleware):
    
    async def on_pre_process_message(self, message: types.Message, data:dict):
        word_count = await get_silent_word_count()
        silent_status= await get_silent()

        if message.text != None and str(message.chat.id) not in ADMIN:
            if word_count!=3:
                await get_silent_word_count(1)
            elif silent_status=='Off':
                await letsplay()


            print('middle checker')
            #print ('SPAM CHECKER MIDDLE')


            if await check_jumper() == 0:
                if "bet" in message.text.lower() and message.chat.type == 'supergroup':
                    await bot.delete_message(CHAT, message.message_id)
                    raise CancelHandler()
                elif "bet" in message.text.lower():
                    await bot.delete_message(message.from_user.id,message.message_id)
                    raise CancelHandler()
                    

    async def on_process_callback_query(self, call: types.CallbackQuery, data:dict):

        if await check_jumper() == 1:
            #print('DATA MIDDLE',data['callback_data']['but'])
            if data['callback_data']['value']=='settings':
                
                await call.answer('самфин вент вронг. трай ит афтер зе рейс')
                raise CancelHandler()


