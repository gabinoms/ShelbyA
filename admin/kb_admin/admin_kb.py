from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB


kb_sched = IKM(
	inline_keyboard=[
	[IKB('Start',callback_data='adm:2:start'),
	 IKB('Pause',callback_data='adm:2:pause')],

	[IKB('Resume',callback_data='adm:2:resume'),
	 IKB('Stop',callback_data='adm:2:shutdown')],
	[IKB('Back',callback_data='adm:2:back')]
	])


	
# cbd_adm = CallbackData('adm','but','value')
admkb_main = IKM(
	inline_keyboard=[
	[IKB('users',callback_data='adm:1:users')],
	[IKB('core',callback_data='adm:1:core')],
	[IKB('base',callback_data='adm:1:base')]
	])