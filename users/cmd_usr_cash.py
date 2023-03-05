# from aiogram.utils.exceptions import MessageNotModified
# from contextlib import suppress
import asyncio
import datetime


from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB

from engine import bot,dp
from config import ADMIN
from .kb_user.currencies_kb import tokens_kb
from .kb_user.players_kb import kb_main

from datas.bh_methods import usr_info, dep_to_balance, check_balance_selected, balance_withdraw, set_deposit, set_deposit_status, set_withdraw, check_vip_status, withdraw_pending
from text.interfaces import profile_info

from admin.payments_methods_alt import dep_create, dep_status_check, get_min_dep, get_min_with, get_main_balance, with_create
from admin.cmd_root import admin_approve


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


# async def kb_w(url):
# 	kb_withdraw = IKM(
# 		inline_keyboard=[[IKB('🎁',url=url)]
# 		])
# 	return kb_withdraw


async def to_cancel(message,state:FSMContext):
	res = await usr_info(message.from_user.id)
	await bot.send_message(message.from_user.id,f'{await profile_info(res[0],res[1],res[2])}',reply_markup = await kb_main(res[1]))
	await bot.delete_message(message.from_user.id,message.message_id)
	await state.finish()


async def to_cancel_cb(call,state:FSMContext):
	res = await usr_info(call.from_user.id)
	await bot.edit_message_text(f'{await profile_info(res[0],res[1],res[2])}',call.from_user.id,call.message.message_id,reply_markup = await kb_main(res[1]))
	await state.finish()

	
async def to_deposit(call):
	await bot.edit_message_text('выберите валюту',call.from_user.id, call.message.message_id,reply_markup = tokens_kb)
	await PSG.st1.set()


async def deposit_token(call,callback_data:dict,state:FSMContext):	

	value = callback_data['value']
	

	if value == 'back':
		
		res = await usr_info(call.from_user.id)
		await bot.edit_message_text(f'{await profile_info(res[0],res[1],res[2])}',call.from_user.id,call.message.message_id,reply_markup = await kb_main(res[1]))
		await state.finish()

	else:

		min_amount = await get_min_dep(value)
		async with state.proxy() as data:
			data['cash'] = value
			data['min_amnt'] = min_amount
			await bot.edit_message_text(f'укажите сумму депозита, (min - {min_amount} {value})\n (<i>введите <code>cancel</code>, чтобы отменить текущее действие</i>)', call.from_user.id, call.message.message_id)
		await PSG.next()
			

async def deposit_amount(message,state:FSMContext):

	async with state.proxy() as data:
		token_name = data['cash']#token
		min_amnt_dep = float(data['min_amnt'])
		usr_amnt_dep = float(message.text)#amount of deposit

	if usr_amnt_dep <= min_amnt_dep:
		amount = min_amnt_dep

	else:
		
		amount = usr_amnt_dep

	inv_id, ext_link = await dep_create(token_name,amount)
	await set_deposit(message.from_user.id,inv_id,token_name,amount,message.date,'pending')

	id_del = await bot.send_message(message.from_user.id,f'<b>ID</b> <code>{inv_id}</code>')
	await bot.send_message(message.from_user.id,f'вы собираетесь внести депозит на сумму {amount} {token_name}\nсохраните id транзакции\n<i>скоро вы будете автоматически перенаправлены в главное меню</i>',reply_markup=await kb(ext_link))

	await asyncio.sleep(30)

	a = await dep_status_check(inv_id)
	

	if a['data']['payments']!=[]:
		dep_uid = a['data']['payments'][0]['userId']
		dep_amount = a['data']['payments'][0]['paymentAmount']
		dep_currency = a['data']['currency']
		dep_date = a['data']['payments'][0]['paid']


		await set_deposit_status(dep_uid,inv_id,'paid')
		await dep_to_balance(dep_uid, dep_currency, dep_amount)
		await id_del.delete()

	else:

		await set_deposit_status(message.from_user.id,inv_id,'not_paid')

	res = await usr_info(message.from_user.id)
	await bot.edit_message_text(f'{await profile_info(res[0],res[1],res[2])}',message.from_user.id,message.message_id+2,reply_markup = await kb_main(res[1]))
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
		await bot.edit_message_text(f'{await profile_info(res[0],res[1],res[2])}',call.from_user.id,call.message.message_id,reply_markup = await kb_main(res[1]))
		await state.finish()

	else:

		min_with = await get_min_with(value)
		async with state.proxy() as data:
			res = await check_balance_selected(call.from_user.id,value)
			
			if float(res)!=0.0 and float(res) < float(min_with):

				await call.answer(f'минимальная сумма вывода - {min_with} {value}\n (чтобы вывести {res} {value} - напишиите администратору)',show_alert=True)


				res1 = await usr_info(call.from_user.id)
				await bot.edit_message_text(f'{await profile_info(res1[0],res1[1],res1[2])}',call.from_user.id,call.message.message_id,reply_markup = await kb_main(res1[1]))
				await state.finish()

			elif float(res)!=0.0 and float(res) >= float(min_with):


				data['with_token'] = value
				data['with_min_amount'] = min_with
				data['with_max_amount'] = res
				await bot.edit_message_text(f'укажите сумму вывода, (min - {min_with} {value}, max - {res} {value})\n (<i>введите <code>cancel</code>, чтобы отменить текущее действие</i>)', call.from_user.id, call.message.message_id)
				await WSG.next()
			else:
				await bot.edit_message_text('Инсуффисиент фундс, ало\n\n', call.from_user.id, call.message.message_id)
				await bot.send_message(call.from_user.id,'выберите валюту',reply_markup = tokens_kb)


async def withdraw_amount(message,state:FSMContext):

	async with state.proxy() as data:
		token = data['with_token']#token
		usr_amnt_with = float(message.text)#amount
		min_amnt_with = float(data['with_min_amount'])#minimum amount of withdraw
		max_amnt_with = float(data['with_max_amount'])#user_balance
		user_id = message.from_user.id
		vip = await check_vip_status(user_id)

		trs_id = str(datetime.datetime.now().timestamp()).replace('.','').replace('1','0').replace('6','3')

		#trs_id = str(user_id)

		main_balance = await get_main_balance(token)#main_balance
	
		if max_amnt_with < main_balance:

			if usr_amnt_with > min_amnt_with:

				if usr_amnt_with > max_amnt_with:
					amount = max_amnt_with
				else:
					amount = usr_amnt_with

			elif usr_amnt_with <= min_amnt_with:

				amount = min_amnt_with

			if vip=='💤':

				await state.finish()
				await bot.send_message(user_id,f'id <code>{trs_id}</code>: Ваша заявка на вывод средств принята в обработку.\n<i>сохраните id транзакции</i>')
				await balance_withdraw(user_id,token,amount)
				await withdraw_pending(user_id, trs_id, token, amount, message.date)

				await admin_approve(user_id, trs_id, token, amount)
				
				await asyncio.sleep(5)
				res = await usr_info(message.from_user.id)
				await bot.send_message(message.from_user.id,f'{await profile_info(res[0],res[1],res[2])}',reply_markup = await kb_main(res[1]))

				
			else:
				chst = await with_create(user_id, trs_id, token, amount)
				await set_withdraw(user_id, chst['data']['id'], chst['data']['currency'], chst['data']['amount'], message.date, chst['success'])
				await balance_withdraw(user_id,token,amount)


				await asyncio.sleep(5)
				res = await usr_info(message.from_user.id)
				await bot.send_message(message.from_user.id,f'{await profile_info(message.from_user.id,res[0],res[1],res[2])}',reply_markup = await kb_main(res[1]))
				await state.finish()
			



		elif usr_amnt_with == main_balance:
			await message.answer('вронг дата. телл зе админ абоут ит')
			await bot.send_message(ADMIN, 'some happened wrong. user balance equal as main balance')
			res = await usr_info(message.from_user.id)
			await bot.send_message(message.from_user.id,f'{await profile_info(res[0],res[1],res[2])}',reply_markup = await kb_main(res[1]))
			await state.finish()

			
		else:
			await message.answer('вронг дата. телл зе админ абоут ит')
			await bot.send_message(ADMIN, ' big amount of withdraw.some happened wrong')
			res = await usr_info(message.from_user.id)
			await bot.send_message(message.from_user.id,f'{await profile_info(res[0],res[1],res[2])}',reply_markup = await kb_main(res[1]))
			await state.finish()









async def spam_remover(message,state:FSMContext):
	if str(message.chat.id) in ADMIN:
		print('spam checker')
		if message.chat.type != 'supergroup':
			if message.text.lower() == 'reload':
				res = await usr_info(message.from_user.id)
				await bot.send_message(message.from_user.id,f'{await profile_info(res[0],res[1],res[2])}',reply_markup = await kb_main(res[1]))
				await state.finish()

			elif message.text.lower()!='cancel' or float(message.text.isdigit())!=True:
				await bot.delete_message(message.from_user.id,message.message_id)