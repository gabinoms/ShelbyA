from aiogram.dispatcher.filters import Text
from engine import dp , cbd_adm
from .cmd_root import USG, admin_panel, admin_panel_refresh, to_core, to_users, to_base, core, users_menu, users_menu_step2, users_menu_dep, users_menu_with, approve_withdraw, decline_withdraw


def setup():
	dp.register_message_handler(admin_panel, commands='admin', commands_prefix='!')

	dp.register_callback_query_handler(to_core, cbd_adm.filter(but=['1'],value=['core']))
	dp.register_callback_query_handler(to_users, cbd_adm.filter(but=['1'],value=['users']))
	dp.register_callback_query_handler(to_base, cbd_adm.filter(but=['1'],value=['base']))
	
	dp.register_callback_query_handler(admin_panel_refresh, cbd_adm.filter(but=['1'],value=['refresh']))
	dp.register_callback_query_handler(core, cbd_adm.filter(but=['2']))
	dp.register_message_handler(users_menu,state=USG.st1)
	dp.register_callback_query_handler(users_menu_step2, cbd_adm.filter(but=['3']),state=USG.st2)
	dp.register_message_handler(users_menu_dep,state=USG.st3)
	dp.register_message_handler(users_menu_with,state=USG.st4)
	
	dp.register_callback_query_handler(approve_withdraw, Text(startswith='aprv_'),state='*')
	dp.register_callback_query_handler(decline_withdraw, Text(startswith='dcln_'),state='*')
