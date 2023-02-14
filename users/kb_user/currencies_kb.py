from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB

tokens_kb = IKM(
	inline_keyboard=[
	[IKB('TON',callback_data='cash:1:41:ton:0.005'),IKB('BOLT',callback_data='cash:1:41:bolt:0.5')],
	[IKB('KISS',callback_data='cash:1:41:kiss:10'),IKB(' ',callback_data='cash:1:41:back:0')],
	[IKB('⬅️ Назад',callback_data='cash:1:41:back:0')]
	])


