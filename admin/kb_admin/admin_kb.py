from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB


# cbd_adm = CallbackData('adm','but','value')
admkb_main = IKM(
	inline_keyboard=[
	[IKB('users',callback_data='adm:1:users'),
	 IKB('core',callback_data='adm:1:core'),
	 IKB('base',callback_data='adm:1:base')],
	[IKB('refresh',callback_data='adm:1:refresh')]
	])



kb_sched = IKM(
	inline_keyboard=[
	[IKB('Start',callback_data='adm:2:start'),
	 IKB('Pause',callback_data='adm:2:pause')],

	[IKB('Resume',callback_data='adm:2:resume'),
	 IKB('Stop',callback_data='adm:2:shutdown')],
	[IKB('SilentOn',callback_data='adm:2:silent_on'),
	 IKB('SilentOff',callback_data='adm:2:silent_off')],
	[IKB('Back',callback_data='adm:2:back')]
	])


admkb_users = IKM(
	inline_keyboard=[
	[IKB('reset state',callback_data='adm:3:reset_state')],
	[IKB('deposit',callback_data='adm:3:dep'),
	 IKB('withdraw',callback_data='adm:3:with')],
	[IKB('find other',callback_data='adm:3:find')],
	[IKB('Back',callback_data='adm:3:backtomain')]
	])
