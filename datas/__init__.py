from peewee import *
from .bh_clases import Race, Bet, User, Ubalance, Udeposit, Uwithdraw, dbase




def setup():
	with dbase:
		dbase.drop_tables([Race,Bet])
		dbase.create_tables([Race, Bet, User, Ubalance, Udeposit, Uwithdraw])
		Race(race_id=0,jumper=0).save(force_insert=True)
