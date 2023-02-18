from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB

tokens_kb = IKM(
	inline_keyboard=[
	[IKB('TON',callback_data='cash:1:41:TON'),IKB('VIRUS',callback_data='cash:1:41:VIRUS')],
	[IKB('KISS',callback_data='cash:1:41:KISS'),IKB(' ',callback_data='cash:1:41:back')],
	[IKB('⬅️ Назад',callback_data='cash:1:41:back')]
	])


