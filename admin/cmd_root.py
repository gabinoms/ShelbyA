from engine import scheduler, dp, bot
from config import ADMIN
import asyncio

from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB
# from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.dispatcher import FSMContext


from .kb_admin.admin_kb import admkb_main , kb_sched
from .payments_methods_alt import get_main_balance, with_create
from datas.bh_methods import players_count, max_user_balance, set_withdraw, get_withdraw_details, withdraw_decline, dep_to_balance, withdraw_pending_remove

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


async def admin_panel(message):
    if str(message.chat.id) in ADMIN:
        await message.answer(await club_main(),reply_markup = admkb_main)


async def to_core(call):    
    await bot.send_message(call.from_user.id,f'scheduler administration',reply_markup = kb_sched)


async def core(call, callback_data:dict):
    value = callback_data['value']
    if value == 'back':
        await bot.edit_message_text(await club_main(),call.from_user.id,call.message.message_id,reply_markup = admkb_main)
    else:
        exec('scheduler.'+value+'()')
        await call.answer(f'scheduler: {value}')
        await bot.edit_message_text(f'scheduler administration',call.from_user.id,call.message.message_id,reply_markup = kb_sched)


async def admin_approve(user_id, trs_id, token, amount):

    await bot.send_message(ADMIN, f'⚠️ Заявка <code>{trs_id}</code> на вывод {user_id} {amount} {token}',reply_markup= await kb_approve(trs_id))



async def approve_withdraw(call):

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


async def decline_withdraw(call):

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



