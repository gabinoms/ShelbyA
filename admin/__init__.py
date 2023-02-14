from engine import dp
from .cmd_root import run, pause, resume, stop

def setup():
	dp.register_message_handler(run , commands='run', commands_prefix='!')
	dp.register_message_handler(pause, commands='pause', commands_prefix='!')
	dp.register_message_handler(resume, commands='resume', commands_prefix='!')
	dp.register_message_handler(stop, commands='stop', commands_prefix='!')
