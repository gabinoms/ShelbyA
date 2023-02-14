from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB

async def kb_main(status):
	

	kb_default = IKM(
		inline_keyboard=[
		[IKB('💵 пополнить',callback_data='pref:1:update_free')],
		[IKB('⚙️ настройки',callback_data='pref:2:settings')],
		[IKB('🔄 обновить',callback_data='pref:2:refresh')]
		])

	kb_cash = IKM(
		inline_keyboard=[
		[IKB('💎 пополнить',callback_data='pref:4:deposit'),
		 IKB('💎 вывести',callback_data='pref:5:withdraw')],
		[IKB('⚙️ настройки',callback_data='pref:2:settings')],
		[IKB('🔄 обновить',callback_data='pref:2:refresh')]
		])

	if status == 'DEMO':
		kb = kb_default
	elif status == 'CAsH':
		kb = kb_cash
	return kb


async def kb_settings(status):
	if status=='DEMO':
		kb = IKM(
			inline_keyboard=[
			[IKB('вкл CAsH',callback_data='pref:3:empty'),
			 IKB('⬅️ назад',callback_data='pref:3:main')]
			])
	elif status=='CAsH':
		kb = IKM(
			inline_keyboard=[
			[IKB('вкл DEMO',callback_data='pref:3:empty'),
			 IKB('выбор счета',callback_data='pref:3:select')],
			[IKB('⬅️ назад',callback_data='pref:3:main')]
			])
	return kb


async def kb_select_token(res):
	kb =IKM(row_width=3)
	backbutton=IKB('⬅️ назад',callback_data='pref:3:main')
	for r in res:
		button = IKB(text=r,callback_data=f'select_{r}')
		kb.insert(button)
	kb.add(backbutton)
	return kb