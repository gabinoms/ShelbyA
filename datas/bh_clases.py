from peewee import *

dbase = SqliteDatabase('datas/bh_data.db')


class BaseMod(Model):
	class Meta:
		database = dbase


class GameMode(BaseMod):

	mode_parameter = CharField(default='mode')#silent
	mode_count = IntegerField(default=0)#count of words
	mode_count_stop = IntegerField(default=0)#count of races without bets
	mode_position = CharField(default='Off')#on off
	
	class Meta:
		db_table = 'gamemodes'


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
	user_ref_link = CharField(default='0')


	class Meta:
		db_table = 'users'

class Referral(BaseMod):

	owner = ForeignKeyField(User)
	ref_id = CharField()
	registration_date = CharField()

	class Meta:
		db_table = 'refs'


class Vip(BaseMod):

	owner = ForeignKeyField(User)
	vip_status = CharField(default='💤')#silver,bronze,gold,platinum
	vip_status_time = CharField(default='0')
	vip_points = FloatField(default=0)
	vip_daily_bonus = DateTimeField(default=0)

	class Meta:
		db_table = 'vip'


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

