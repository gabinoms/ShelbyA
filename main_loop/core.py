import asyncio
import random
from engine import dp,bot,scheduler
from config import CHAT, road

from datas.bh_methods import race_create, get_race_result, calculate2, get_winners, get_current_race, race_close, calculate_bets
from .ada_moves import stopgame

import time


from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress


async def alarm1(dp):


    async def horse(i, mes):
        a = mes.rjust(i,'_').ljust(20,'_')

        return a

    #x = ('1️⃣','2️⃣','3️⃣','4️⃣','5️⃣')
    x =(1, 2, 3, 4, 5)
    final=[]  
    h = dict.fromkeys(x,20)
    acc2 = dict.fromkeys(x,0)
    acc3 = dict.fromkeys(x,0)
    ro = dict.fromkeys(x,0)
   
    for i in acc2.keys():
        acc2[i]=random.randint(0,1)
        acc3[i]=random.randint(0,2)


    


    await dp.bot.set_chat_permissions(chat_id=CHAT,permissions ={'can_send_messages': True})
    await dp.bot.send_message(chat_id=CHAT,text="Делайте ваши ставки")
    
    race_number = await race_create()
    

    await asyncio.sleep(25)
    await dp.bot.set_chat_permissions(chat_id=CHAT,permissions ={'can_send_messages': False})
    await bot.send_message(chat_id=CHAT,text=f"Ставки сделаны. Ставок больше нет.\n\nНачинается заезд <code>#{race_number}</code>")
    

    

    a=await bot.send_message(chat_id=CHAT,text=f'💤{road}\n'*5)


    
    k=20
    while k >=0 :
        with suppress(MessageNotModified):
            await asyncio.sleep(1.2)#1.2
            await bot.edit_message_text(f"1️⃣{await (horse(h[1],'🏇'))}\n2️⃣{await (horse(h[2],'🏇'))}\n3️⃣{await (horse(h[3],'🏇'))}\n4️⃣{await (horse(h[4],'🏇'))}\n5️⃣{await (horse(h[5],'🏇'))}",CHAT,a['message_id'])

        for f in h.keys():
            if h[f]<=1:
                if f not in final:
                    final.append(f)


        if k >= 19:
            for x1 in h.keys():
                h[x1]-=acc3[x1]


        elif k >=14:
            for x1 in h.keys():
                h[x1]-=acc2[x1]

        elif k >= 4 and k <= 5:
            win1 = dict(sorted(h.items(), key=lambda item: item[1]))
            win = tuple(win1)
            ######winners win[0] - win[4]

            
            await calculate2(win[0],win[1],win[2],race_number)
            await get_race_result(win[0],win[1],win[2])



        for i in h.keys():
            h[i]-=2

        k-=2




    await asyncio.sleep(2)
    await bot.send_message(chat_id=CHAT,text=f'<code>#{race_number}</code>\nРезультаты:\n🏆 - {win[0]}\t🥈 - {win[1]}\t🥉 - {win[2]}\n\n\t\t\t\t\t\t\t\t🏅 - {win[3]}\t\t\t🏅 - {win[4]}')
    winners_list=''
    wnrs = await get_winners()
    if len(wnrs)==0:
        winners_list='а никто не играл🤔'
    elif len(wnrs)<=5:
        for w in range(len(wnrs)):
            winners_list+=f'🍾{wnrs.pop() }'

    await bot.send_message(chat_id=CHAT,text=f'<code>#{race_number}</code>\nпобедители:\n {winners_list}')


    count_of_bets = await calculate_bets(race_number)
    if count_of_bets == 0:
        await stopgame()
    await race_close()


    

    




    await dp.bot.set_chat_permissions(chat_id=CHAT,permissions ={'can_send_messages': True})


 