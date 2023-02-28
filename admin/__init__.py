from aiogram.dispatcher.filters import Text
from engine import dp , cbd_adm
from .cmd_root import admin_panel, to_core, core, approve_withdraw, decline_withdraw


def setup():
	dp.register_message_handler(admin_panel, commands='admin', commands_prefix='!')

	dp.register_callback_query_handler(to_core, cbd_adm.filter(but=['1'],value=['core']))
	dp.register_callback_query_handler(core, cbd_adm.filter(but=['2']))
	
	dp.register_callback_query_handler(approve_withdraw, Text(startswith='aprv_'))
	dp.register_callback_query_handler(decline_withdraw, Text(startswith='dcln_'))
