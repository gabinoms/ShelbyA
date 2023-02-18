import asyncio
from aiogram.utils.exceptions import Throttled, BotBlocked, CantInitiateConversation
from engine import bot,dp
from config import CHAT




from datas.bh_methods import usr_exists, usr_add, usr_info, check_balance, update_balance, get_current_race, set_user_bet, get_winners, update_status_account, set_current_wallet, get_active_wallets, set_active_wallet, race_create

from .kb_user.players_kb import kb_main, kb_settings, kb_select_token
from text.interfaces import profile_info, settings_info

from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress
from admin.payments_methods_alt import get_main_balance



async def to_begin(message):
    try:

        if await usr_exists(message.from_user.id) == None:
            await usr_add(message.from_user.id, message.from_user.first_name)
        res = await usr_info(message.from_user.id)
        await bot.send_message(message.from_user.id,f'{await profile_info(message.from_user.id,res[0],res[1],res[2],res[3],res[4])}',reply_markup = await kb_main(res[2]))
        await bot.delete_message(message.chat.id,message.message_id)
        # a=await get_main_balance('virus')
        # print(type(a))



       

    except (BotBlocked, CantInitiateConversation):
        await message.reply('напиши мне в личку, у меня спамблок')
        await asyncio.sleep(5)
        await bot.delete_message(message.chat.id,message.message_id+1)
        await bot.delete_message(message.chat.id,message.message_id)
        #!!!IMPORTANT!!!
        #запилить удаление юзверя из базы бота,в случае блока


    # except CantInitiateConversation:
    #     await message.reply('напиши мне в личку, у меня спамблок')
    #     await asyncio.sleep(5)
    #     await bot.delete_message(message.chat.id,message.message_id+1)
    #     await bot.delete_message(message.chat.id,message.message_id)

async def to_account(message):
    res = await usr_info(message.from_user.id)

    await bot.send_message(message.from_user.id,f'{await profile_info(message.from_user.id,res[0],res[1],res[2],res[3],res[4])}',reply_markup = await kb_main(res[2]))
    await bot.delete_message(message.chat.id,message.message_id)

    


#  a =  bet1 123
#  a[3:4] - number of horse 
#  a[4:5] - space symbol
#  a[5:]  - bet amount
#
#


async def place_bet(message):
    betting_text = message.text

    if message.chat.type == 'supergroup':
        if betting_text[4:5] != ' ':


            await bot.send_message(message.chat.id,f'{message.from_user.first_name}, неверный формат ставки. Формат ставки:<b> bet* **</b>\n<i>где * - номер лошади, ** - сумма ставки. Например <code>bet1 1000</code> или  <code>bet1 1.234</code></i>')
            await bot.delete_message(message.from_user.id, message.message_id)

            
        elif not (betting_text[5:]).replace('.','',1).isdigit() or not (betting_text[3:4]).isdigit() or int(betting_text[3:4])>5:

            await message.reply('невалуйные ставки = нещадный бан')
            #await bot.delete_message(message.chat.id, message.message_id)
        else:
            usr_bet = float(betting_text[5:])
            bet_horse = int(betting_text[3:4])
            usr_bal, usr_token = await check_balance(message.from_user.id)
            usr_curr ='💵' if usr_token=='DEMO' else usr_token 
            current_race = await get_current_race()
            if usr_bet<=usr_bal:
                await message.answer(f'{message.from_user.first_name} поставил <code>{message.text[5:]} <b>{usr_token}</b></code> на номер <code>{message.text[3:4]}</code>')
                await update_balance(message.from_user.id,-usr_bet)
                await set_user_bet(current_race,message.from_user.id,usr_bet,bet_horse)
            else:
                await message.answer("инсуффисиент фундс")
               #########delete message insert here############

    else:
        await message.answer('Лайв-ставки принимаются в общем чате')
        #await bot.delete_message(message.chat.id,message.message_id)


async def up_demo(call,callback_data:dict):
    value = callback_data['value']
    usr_bal, usr_token = await check_balance(call.from_user.id)

    if value == 'update_free':
        if usr_bal <=0:
            await update_balance(call.from_user.id, 1000)
            res = await usr_info(call.from_user.id)
            await bot.edit_message_text(f'{await profile_info(call.from_user.id,res[0],res[1],res[2],res[3],res[4])}',call.from_user.id,call.message.message_id,reply_markup = await kb_main(res[2]))
            await call.answer('ваш 🪙 счет успешно пополнен. приятного отдыха')

        elif usr_bal > 0:
            await call.answer('😐')
            
@dp.throttled(rate=2)
async def refresh(call):
    with suppress(MessageNotModified):
        res = await usr_info(call.from_user.id)
        await bot.edit_message_text(f'{await profile_info(call.from_user.id,res[0],res[1],res[2],res[3],res[4])}',call.from_user.id,call.message.message_id,reply_markup = await kb_main(res[2]))
    await call.answer()

async def settings(call):

    res = await usr_info(call.from_user.id)
    #print(call)
    await bot.edit_message_text(await settings_info(call.from_user.id,res[2]), call.from_user.id, call.message.message_id,reply_markup = await kb_settings(res[2]))
    await call.answer()

@dp.throttled(rate=1)
async def settings_mode(call,callback_data:dict):
    #print(call)

    value = callback_data['value']
    res = await usr_info(call.from_user.id)
    
    if value == 'empty':

        
        res_upd = await update_status_account(call.from_user.id,'DEMO' if res[2]!='DEMO' else 'CAsH')
        await set_current_wallet(call.from_user.id, res_upd)
        with suppress(MessageNotModified):
            await bot.edit_message_text(await settings_info(call.from_user.id,res_upd),call.from_user.id, call.message.message_id,reply_markup = await kb_settings(res_upd))
            await call.answer()


    elif value == 'select':
        # res = await usr_info(call.from_user.id)
        # with suppress(MessageNotModified):
        #     await bot.edit_message_text(await settings_info(call.from_user.id,res),call.from_user.id, call.message.message_id,reply_markup = await kb_settings(res))
        #     await call.answer()
        res_act = await get_active_wallets(call.from_user.id)
        await bot.edit_message_text(f'здесь можете изменить основной счет\nваш текущий счет - <code>{res[3]}</code>',call.from_user.id,call.message.message_id,reply_markup=await kb_select_token(res_act))
        

    elif value == 'main':
        #res = await usr_info(call.from_user.id)
        await bot.edit_message_text(f'{await profile_info(call.from_user.id,res[0],res[1],res[2],res[3],res[4])}',call.from_user.id,call.message.message_id,reply_markup = await kb_main(res[2]))
    await call.answer()


async def select_wallet(call):
    res = call.data.split('_')[1]
    if res!='****':
        await set_active_wallet(call.from_user.id,res)
        await call.answer(f'ваш текущий счет изменен на {res}. приятного отдыха')

    else:
        await call.answer('здесь можно будет добавлять свои токены')
        
    res1 = await usr_info(call.from_user.id)
    await bot.edit_message_text(f'{await profile_info(call.from_user.id,res1[0],res1[1],res1[2],res1[3],res1[4])}',call.from_user.id,call.message.message_id,reply_markup = await kb_main(res1[2]))
