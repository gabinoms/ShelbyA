from aiogram.dispatcher.filters import Text
from engine import dp, cbd_cash, cbd_cash1

from .cmd_usr import to_begin, to_account, place_bet, up_demo, refresh, settings, settings_mode, select_wallet
from .cmd_usr_cash import PSG, WSG, to_deposit, deposit_token, to_cancel, deposit_amount, to_cancel_cb, spam_remover, to_withdraw, withdraw_token, withdraw_amount

def setup():
	dp.register_message_handler(to_begin,commands=['start'])
	dp.register_message_handler(to_account,commands=['acc'])
	dp.register_message_handler(place_bet,Text(startswith='bet',ignore_case=True))
	dp.register_callback_query_handler(up_demo, cbd_cash.filter(but=['1']))
	dp.register_callback_query_handler(refresh, cbd_cash.filter(but=['2'],value=['refresh']))
	dp.register_callback_query_handler(settings, cbd_cash.filter(but=['2']))
	dp.register_callback_query_handler(settings_mode, cbd_cash.filter(but=['3']))
	dp.register_callback_query_handler(select_wallet,Text(startswith='select_'))

	#############################################################################
	#                               CAsH handlers                               #
	#############################################################################
	#                                  deposit                                  #
	#############################################################################
	dp.register_callback_query_handler(to_deposit, cbd_cash.filter(but=['4']))
	dp.register_callback_query_handler(deposit_token, cbd_cash1.filter(jump=['1'],but=['41']),state=PSG.st1)
	dp.register_message_handler(to_cancel,Text(equals='cancel'),state=PSG.st2)
	dp.register_message_handler(deposit_amount,regexp = r'^[-+]?[0-9]*[.,]?[0-9]+(?:[eE][-+]?[0-9]+)?$',state=PSG.st2)
	dp.register_callback_query_handler(to_cancel_cb,cbd_cash1.filter(jump=['1'],but=['42']),state=PSG.st2)
	
    #############################################################################
	#                               CAsH handlers                               #
	#############################################################################
	#                                  withdraw                                 #
	#############################################################################
	dp.register_callback_query_handler(to_withdraw,cbd_cash.filter(but=['5']))
	dp.register_callback_query_handler(withdraw_token,cbd_cash1.filter(jump=['1']),state=WSG.st1)
	dp.register_callback_query_handler(to_cancel_cb,cbd_cash1.filter(jump=[1]),state=WSG.st1)

	dp.register_message_handler(to_cancel,Text(equals='cancel'),state=WSG.st2)
	dp.register_message_handler(withdraw_amount,regexp = r'^[-+]?[0-9]*[.,]?[0-9]+(?:[eE][-+]?[0-9]+)?$',state=WSG.st2)
	
	##########################  SPAM_REMOVER_HANDLER  ###########################
	dp.register_message_handler(spam_remover,state='*')
