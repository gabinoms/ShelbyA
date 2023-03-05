from peewee import *
from .bh_clases import GameMode,Race, Bet, User, Referral, Vip, Ubalance, Udeposit, Uwithdraw, dbase




def setup():
	with dbase:
		dbase.drop_tables([Race,Bet])
		dbase.create_tables([GameMode,Race, Bet, User, Referral, Vip, Ubalance, Udeposit, Uwithdraw])
		Race(race_id=0,jumper=0).save(force_insert=True)
		GameMode(mode_parameter = 'Silent', mode_count=0, mode_count_stop=0, mode_position='Off').save(force_insert=True)
