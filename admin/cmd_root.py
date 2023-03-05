from engine import scheduler, dp, bot
from config import ADMIN, CHAT, stick01, stick02
import asyncio

from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress

from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


from .kb_admin.admin_kb import admkb_main, admkb_users, kb_sched
from .payments_methods_alt import get_main_balance, with_create
from datas.bh_methods import players_count, max_user_balance, set_withdraw, get_withdraw_details, withdraw_decline,\
 dep_to_balance, balance_withdraw, withdraw_pending_remove, usr_info, usr_info_all, check_vip_info, set_silent, get_silent, get_silent_word_count
from text.interfaces import profile_info
from users.kb_user.players_kb import kb_main


class USG(StatesGroup):
    st1 = State()
    st2 = State()
    st3 = State()
    st4 = State()

status={0:'stopped', 1:'running', 2:'waiting'}

async def kb_approve(transid):

    kb =IKM(
        inline_keyboard=[
        [IKB('Approve',callback_data=f'aprv_{transid}'),
         IKB('Decline',callback_data=f'dcln_{transid}')]
        ])
    return kb






async def club_main():

    players = await players_count()
    balances = await max_user_balance()

    main_balance = await get_main_balance()

    res = f"""• Golden Horse Club •
users total: <code>{players}</code>\t\t\t\trace status: <code>{status[scheduler.state]}</code>

<code>{main_balance}</code>
<i>most rich players and his balance</i>:
{balances}
    """
    return res

########################################################################
#           ADMIN PANEL     
########################################################################
#                          ALL SEGMENTS
########################################################################

async def admin_panel(message):
    if str(message.chat.id) in ADMIN:
        await message.answer(await club_main(),reply_markup = admkb_main)
        await bot.delete_message(ADMIN, message.message_id)

async def admin_panel_refresh(call):
    with suppress(MessageNotModified):
        await bot.edit_message_text(await club_main(),call.from_user.id,call.message.message_id, reply_markup = admkb_main)
    await call.answer('refreshed')

########################################################################
#           ADMIN PANEL     
########################################################################
#                           CORE
########################################################################

async def to_core(call):    
    await bot.edit_message_text(f'scheduler administration\nrace status: <code>{status[scheduler.state]}</code>\nsilent mode: <code>{await get_silent()}</code>',call.from_user.id, call.message.message_id,reply_markup = kb_sched)


async def core(call, callback_data:dict):
    value = callback_data['value']
    if value == 'back':
        await bot.edit_message_text(await club_main(),call.from_user.id,call.message.message_id,reply_markup = admkb_main)

    elif value == 'silent_on':
        
        await bot.send_sticker(CHAT,sticker=stick01)
        await set_silent('On')


    elif value == 'silent_off':
        
        await bot.send_sticker(CHAT,sticker=stick02)
        await set_silent('Off')


    else:
        exec('scheduler.'+value+'()')
        await call.answer(f'scheduler: {value}')
        await bot.edit_message_text(f'scheduler administration\nrace status: <code>{status[scheduler.state]}</code>',call.from_user.id, call.message.message_id,reply_markup = kb_sched)
    await call.answer()




########################################################################
#           ADMIN PANEL     
########################################################################
#                           USERS
########################################################################



async def to_users(call):
    await bot.edit_message_text(f'users total: <code>{await players_count()}</code>\nenter uid',call.from_user.id,call.message.message_id)
    await USG.st1.set()


async def users_menu(message,state:FSMContext):
    
    if message.forward_from == None:
        if message.text.isdigit():
            uid = message.text
        else:
            uid = 0
    else:
        uid = message.forward_from.id

    userId, userName, userBalance = await usr_info_all(uid)
    vip = await check_vip_info(uid)
    if userId=='ne' and userName=='ne' and userBalance=='ne':
        await bot.send_message(ADMIN,'user not found')
        await bot.send_message(ADMIN,f'users total: <code>{await players_count()}</code>\nenter uid')

    else:

        uState = dp.current_state(chat=uid,user=uid)
        userState = await uState.get_state()

        await bot.delete_message(ADMIN, message.message_id)
        await bot.send_message(ADMIN,f'<code>{userId}</code> {userName}\nVIP {vip[0]} \n<i>current state:</i> <code>{userState}</code>\n\n{userBalance}',reply_markup=admkb_users)
        async with state.proxy() as data:
            data['userId'] = uid
        await USG.next()


async def users_menu_step2(call, callback_data:dict, state:FSMContext):
    async with state.proxy() as data:
        uid = data['userId']

    value = callback_data['value']

    if value == 'backtomain':
        
        await bot.edit_message_text(await club_main(),call.from_user.id,call.message.message_id, reply_markup = admkb_main)
        await state.finish()

    elif value == 'find':
        
        await bot.edit_message_text(f'users total: <code>{await players_count()}</code>\nenter uid',call.from_user.id,call.message.message_id)
        await USG.previous()
        await call.answer()

    elif value == 'reset_state':

        uState = dp.current_state(chat=uid,user=uid)
        await uState.finish()

        res = await usr_info(uid)
        await bot.send_message(uid,f'{await profile_info(res[0],res[1],res[2])}',reply_markup = await kb_main(res[1]))

        userId, userName, userBalance = await usr_info_all(uid)
        
        uState1 = dp.current_state(chat=uid,user=uid)
        userState1 = await uState1.get_state()

        with suppress(MessageNotModified):
            await bot.edit_message_text(f'<code>{userId}</code> {userName}\nVIP {vip[0]} \n<i>current state:</i> <code>{userState1}</code>\n\n{userBalance}',call.from_user.id,call.message.message_id,reply_markup=admkb_users)
        #await USG.previous()
        await call.answer()

    elif value == 'dep':

        await bot.send_message(ADMIN,f'enter token & amount to deposit to account <code>{uid}</code>')
        await USG.next()

    elif value == 'with':

        await bot.send_message(ADMIN,f'enter token & amount to withdraw from account <code>{uid}</code>')
        await USG.st4.set()
    
        


async def users_menu_dep(message,state:FSMContext):
    async with state.proxy() as data:
        uid = data['userId']
    label, amount = message.text.split(' ')[0], message.text.split(' ')[1]

    await dep_to_balance(uid,label,amount)
    await bot.edit_message_text(await club_main(),message.from_user.id, message.message_id, reply_markup = admkb_main)
    await state.finish()


async def users_menu_with(message,state:FSMContext):
    stat = await state.get_state()
    #print('WITHDRAW',stat)

    await balance_withdraw(uid,toke,value)
    await state.finish()



########################################################################
#           ADMIN PANEL     
########################################################################
#                           BASE
########################################################################

async def to_base(call):
    await bot.send_document(ADMIN, document=open('datas/bh_data.db', 'rb')) 



##################################################################################################
#                                 APPROVE OR DECLINE WITHDRAW                                    #
##################################################################################################


async def admin_approve(user_id, trs_id, token, amount):

    await bot.send_message(ADMIN, f'⚠️ Заявка <code>{trs_id}</code> на вывод {user_id} {amount} {token}',reply_markup= await kb_approve(trs_id))



async def approve_withdraw(call, state:FSMContext):

    trs_id = call.data.split('_')[1]    #trans_id

    
    user_id, token, amount, status = await get_withdraw_details(trs_id)# owner, currency, amount, status
    if status=='Pending':
        chst = await with_create(user_id, trs_id, token, amount)
        await set_withdraw(user_id, chst['data']['id'], chst['data']['currency'], chst['data']['amount'], call.message.date, chst['success'])
        await withdraw_pending_remove(trs_id,'Paid')
        inf_mes = await bot.send_message(user_id,f'заявка <code>{trs_id}</code> на вывод {amount} {token} одобрена🙃')
        await call.answer()
        

    elif status=='True' or status=='Paid':
        await call.answer('⚠️уже выплачено, ало')
    else:
        await call.answer('⚠️заявка была отклонена')

    await bot.delete_message(call.from_user.id,call.message.message_id)
    # await asyncio.sleep(3)
    # await inf_mes.delete()


async def decline_withdraw(call, state:FSMContext):

    trs_id = call.data.split('_')[1]
    user_id, token, amount, status = await get_withdraw_details(trs_id)

    if status=='Pending':
        await withdraw_decline(trs_id)
        inf_mes = await bot.send_message(user_id,f'заявка <code>{trs_id}</code> на вывод {amount} {token} отклонена. ваши средства возвращены на игровой баланс')
        await dep_to_balance(user_id,token,amount)
        await call.answer()
    elif status=='True' or status=='Paid':
        await call.answer('⚠️уже выплачено, ало')
    else:
        await call.answer('⚠️заявка уже отклонена')

    await bot.delete_message(call.from_user.id,call.message.message_id)
    # await asyncio.sleep(3)
    # await inf_mes.delete()



