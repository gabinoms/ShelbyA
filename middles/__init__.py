from engine import dp
from .check_bet_middle import BetMiddle

def setup():
	dp.middleware.setup(BetMiddle())