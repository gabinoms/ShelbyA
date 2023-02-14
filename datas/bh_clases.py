from peewee import *

dbase = SqliteDatabase('datas/bh_data.db')


class BaseMod(Model):
	class Meta:
		database = dbase


class Race(BaseMod):

	race_id = BigAutoField(primary_key=True)
	jumper = IntegerField(default=0)
	win1 = IntegerField(default=0)
	win2 = IntegerField(default=0)
	win3 = IntegerField(default=0)

	class Meta:
		db_table = 'races'


class Bet(BaseMod):

	bet_id = IntegerField()
	user_id = BigIntegerField(null=False)
	user_bet_value = FloatField()
	user_bet_horse = IntegerField()
	bet_status = IntegerField(default=0)

	class Meta:
		db_table = 'bets'


class User(BaseMod):

	user_id = BigIntegerField(primary_key=True)
	user_name = CharField(default='plaYer')
	label = CharField(default='DEMO')#DEMO or CAsH
	#user_vip_status = IntegerField(default=0)


	class Meta:
		db_table = 'users'


class Ubalance(BaseMod):

	owner = ForeignKeyField(User)
	token = CharField()
	amount = FloatField(default=0)
	marker = IntegerField(default=0)


	class Meta:
		db_table='balances'

class Udeposit(BaseMod):

	owner = ForeignKeyField(User)	
	trans_id = CharField()
	currency = CharField()
	amount = FloatField(default=0)
	date = CharField()
	status = CharField() 


	class Meta:
		db_table='deposits'


class Uwithdraw(BaseMod):

	owner = ForeignKeyField(User)
	trans_id = CharField()
	currency = CharField()
	amount = FloatField(default=0)
	date = CharField()
	status = CharField() 


	class Meta:
		db_table='withdraws'
