# from aiogram.utils.exceptions import MessageNotModified
# from contextlib import suppress
import asyncio
#from aiogram.utils.exceptions import CancelledError

from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB

from engine import bot,dp
from config import ADMIN
from .kb_user.currencies_kb import tokens_kb
from .kb_user.players_kb import kb_main

from datas.bh_methods import usr_info, dep_to_balance, check_balance_selected, balance_withdraw, set_deposit, set_deposit_status, set_withdraw
from text.interfaces import profile_info

from admin.payments_methods import dep_create, dep_status_check, get_main_balance, with_create, with_status


class PSG(StatesGroup):
    st1 = State()#choice currencie
    st2 = State()#enter amount
    st3 = State()#confirm

class WSG(StatesGroup):
	st1 = State()
	st2 = State()
	st3 = State()
	

async def kb(url):
	kb_confirm = IKM(
		inline_keyboard=[
		[IKB('подтвердить',url=url)]
		#[IKB('отмена',callback_data='cash:1:42:back:0')]
		])
	return kb_confirm


async def kb_w(url):
	kb_withdraw = IKM(
		inline_keyboard=[[IKB('🎁',url=url)]
		])
	return kb_withdraw


async def to_cancel(message,state:FSMContext):
	res = await usr_info(message.from_user.id)
	await bot.send_message(message.from_user.id,f'{await profile_info(message.from_user.id,res[0],res[1],res[2],res[3],res[4])}',reply_markup = await kb_main(res[2]))
	await bot.delete_message(message.from_user.id,message.message_id)
	await state.finish()


async def to_cancel_cb(call,state:FSMContext):
	res = await usr_info(call.from_user.id)
	await bot.edit_message_text(f'{await profile_info(call.from_user.id,res[0],res[1],res[2],res[3],res[4])}',call.from_user.id,call.message.message_id,reply_markup = await kb_main(res[2]))
	await state.finish()

	
async def to_deposit(call):
	await bot.edit_message_text('выберите валюту',call.from_user.id, call.message.message_id,reply_markup = tokens_kb)
	await PSG.st1.set()


async def deposit_token(call,callback_data:dict,state:FSMContext):	

	value = callback_data['value']
	min_amount = callback_data['min_am']

	if value == 'back':
		
		res = await usr_info(call.from_user.id)
		await bot.edit_message_text(f'{await profile_info(call.from_user.id,res[0],res[1],res[2],res[3],res[4])}',call.from_user.id,call.message.message_id,reply_markup = await kb_main(res[2]))
		await state.finish()

	else:
		async with state.proxy() as data:
			data['cash'] = callback_data['value']
			data['min_amnt']=callback_data['min_am']
			await bot.edit_message_text(f'укажите сумму депозита, (min - {min_amount} {value})\n (<i>введите <code>cancel</code>, чтобы отменить текущее действие</i>)', call.from_user.id, call.message.message_id)
		await PSG.next()
			

async def deposit_amount(message,state:FSMContext):

	async with state.proxy() as data:
		value = data['cash']#token
		min_amnt_dep = float(data['min_amnt'])
		usr_amnt_dep = float(message.text)#amount of deposit
	if usr_amnt_dep <= min_amnt_dep:
		amount = min_amnt_dep

	else:
		amount = usr_amnt_dep

	inv_id,ext_link = await dep_create(value,amount)
	await set_deposit(message.from_user.id,inv_id,value,amount,message.date,'pending')

	id_del = await bot.send_message(message.from_user.id,f'<b>ID</b> <code>{inv_id}</code>')
	await bot.send_message(message.from_user.id,f'вы собираетесь внести депозит на сумму {amount} {value}\nсохраните id транзакции',reply_markup=await kb(ext_link))

	await asyncio.sleep(15)

	# curret_state = await state.get_state()
	# if curret_state is None:
	# 	return
	# else:

	try:
		a = await dep_status_check(inv_id)


	except asyncio.CancelledError:

		await asyncio.sleep(1)
		a = await dep_status_check(inv_id)



	if a['payments']!=[]:
		dep_uid = a['payments'][0]['telegram_id']
		dep_amount = a['payments'][0]['amount']
		dep_currency = a['currency'].upper()
		dep_date = a['created']


		await set_deposit_status(dep_uid,inv_id,'paid')
		await dep_to_balance(dep_uid, dep_currency, dep_amount)
		await id_del.delete()

	else:

		await set_deposit_status(message.from_user.id,inv_id,'not_paid')

	res = await usr_info(message.from_user.id)
	await bot.edit_message_text(f'{await profile_info(message.from_user.id,res[0],res[1],res[2],res[3],res[4])}',message.from_user.id,message.message_id+2,reply_markup = await kb_main(res[2]))
	await state.finish()


###########################################################################################################
	
###########################################################################################################

async def to_withdraw(call):
	await bot.edit_message_text('выберите валюту',call.from_user.id, call.message.message_id,reply_markup = tokens_kb)
	await WSG.st1.set()


async def withdraw_token(call,callback_data:dict,state:FSMContext):	

	value = callback_data['value']
	
	if value == 'back':
		
		res = await usr_info(call.from_user.id)
		await bot.edit_message_text(f'{await profile_info(call.from_user.id,res[0],res[1],res[2],res[3],res[4])}',call.from_user.id,call.message.message_id,reply_markup = await kb_main(res[2]))
		await state.finish()

	else:
		async with state.proxy() as data:
			res = await check_balance_selected(call.from_user.id,value)
			
			if float(res)!=0.0:
				data['with_token'] = value
				data['with_max_amount'] = res
				await bot.edit_message_text(f'укажите сумму вывода, (max - {res} {value})\n (<i>введите <code>cancel</code>, чтобы отменить текущее действие</i>)', call.from_user.id, call.message.message_id)
			else:
				await bot.edit_message_text('Инсуффисиент фундс, ало\n\n', call.from_user.id, call.message.message_id)
				await bot.send_message(call.from_user.id,'выберите валюту',reply_markup = tokens_kb)
		await WSG.next()


async def withdraw_amount(message,state:FSMContext):

	async with state.proxy() as data:
		token = data['with_token']#token
		usr_amnt_with = float(message.text)#amount
		max_amnt_with = float(data['with_max_amount'])#user_balance

		main_balance = await get_main_balance(token)#main_balance


		if usr_amnt_with < main_balance:
			if usr_amnt_with > max_amnt_with:
				amount = max_amnt_with
			else:
				amount = usr_amnt_with

			try:
				chid, ext_link = await with_create(token,amount)
				chst = await with_status(chid)
				await set_withdraw(message.from_user.id, chid, token, amount, message.date, chst)

			except asyncio.CancelledError:

				await asyncio.sleep(1)
				chid, ext_link = await with_create(token,amount)
				chst = await with_status(chid)
				await set_withdraw(message.from_user.id, chid, token, amount, message.date, chst)


			await balance_withdraw(message.from_user.id,amount)
			await message.answer('вывод подтвержден',reply_markup = await kb_w(ext_link))
			await asyncio.sleep(10)
			
			chst = await with_status(chid)
			await set_withdraw(message.from_user.id, chid, token, amount, message.date, chst)
			
			res = await usr_info(message.from_user.id)
			await bot.send_message(message.from_user.id,f'{await profile_info(message.from_user.id,res[0],res[1],res[2],res[3],res[4])}',reply_markup = await kb_main(res[2]))



		elif usr_amnt_with == main_balance:
			await message.answer('вронг дата. телл зе админ абоут ит')
			await bot.send_message(ADMIN, 'som happened wrong')
			res = await usr_info(message.from_user.id)
			await bot.send_message(message.from_user.id,f'{await profile_info(message.from_user.id,res[0],res[1],res[2],res[3],res[4])}',reply_markup = await kb_main(res[2]))
			
		else:
			await message.answer('вронг дата. телл зе админ абоут ит')
			await bot.send_message(ADMIN, ' big amount of withdraw.som happened wrong')
			res = await usr_info(message.from_user.id)
			await bot.send_message(message.from_user.id,f'{await profile_info(message.from_user.id,res[0],res[1],res[2],res[3],res[4])}',reply_markup = await kb_main(res[2]))









async def spam_remover(message,state:FSMContext):
	if message.chat.type != 'supergroup':
		if message.text.lower() == 'reload':
			res = await usr_info(message.from_user.id)
			await bot.send_message(message.from_user.id,f'{await profile_info(message.from_user.id,res[0],res[1],res[2],res[3],res[4])}',reply_markup = await kb_main(res[2]))
			await state.finish()
			
		elif message.text.lower()!='cancel' or float(message.text.isdigit())!=True:
			await bot.delete_message(message.from_user.id,message.message_id)