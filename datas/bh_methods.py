from .bh_clases import dbase, Race, Bet, Ubalance, Udeposit, Uwithdraw, User



######################### USER #########################

async def usr_exists(uid):
	with dbase:
		try:
			res = User.select().where(User.user_id == uid).get()
		except User.DoesNotExist:
			res = None
	return res


async def usr_add(uid, uname):
	with dbase.atomic():
		data = [(uid,'DEMO',1000,1),
				(uid,'TON',0,2),
				(uid,'VIRUS',0,2),
				(uid,'KISS',0,2),
				(uid,'****',0,2)]
		

		User.create(user_id=uid, user_name=uname)
		Ubalance.insert_many(data, fields=[Ubalance.owner,Ubalance.token,Ubalance.amount,Ubalance.marker]).execute()
		


async def usr_info(uid):
	with dbase:
		res = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.marker==1).get()
		amount_ed = format(res.amount, '.1f')
		return res.owner.user_id, res.owner.user_name, res.owner.label, res.token, amount_ed


async def update_status_account(uid,label):
	with dbase:
		res = User.select().where(User.user_id==uid).get()
		res.label=label
		res.save()
		return res.label


async def set_current_wallet(uid,label):
	with dbase.atomic():
		if label=='CAsH':
			res = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.token=='DEMO').get()
			res.marker=0
			res.save()
			res1 = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.marker==2).get()
			if res1.marker!='None':
				res1.marker=1
				res1.save()
			else:
				res1 = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.token=='TON').get()
				res1.marker=1
				res1.save()

		elif label=='DEMO':
			res = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.marker==1).get()
			if res.marker!='None':
				res.marker=2
				res.save()
			else:
				pass
			res1 = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.token=='DEMO').get()
			res1.marker=1
			res1.save()

async def get_active_wallets(uid):
	with dbase:
		res = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.token!='DEMO',Ubalance.marker!=1).execute()
		return [a.token for a in res]


async def set_active_wallet(uid,label):
	with dbase:
		res = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.marker==1).get()
		res.marker=2
		res.save()
		res1 = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.token==label).get()
		res1.marker=1
		res1.save()
		

		

######################### CASH #########################

async def check_balance(uid):
	with dbase:
		res = Ubalance.select().join(User).where(User.user_id == uid,Ubalance.marker==1).get()
		return res.amount, res.token


async def check_balance_selected(uid,label):
	with dbase:
		res = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.token==label.upper()).get()
		amount_ed = format(res.amount, '.1f')
		return amount_ed


async def update_balance(uid, value):
	with dbase:
		#User.update(user_balance = User.user_balance+value).where(User.user_id==uid).execute()
		res = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.marker==1).get()
		res.amount+=value
		res.save()


async def balance_withdraw(uid,token,value):
		with dbase:
			#User.update(user_balance = User.user_balance+value).where(User.user_id==uid).execute()
			res = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.token==token).get()
			res.amount-=abs(value)
			res.save()


async def dep_to_balance(uid,label,amount):
	with dbase:
		res_d = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.token==label).get()
		res_d.amount+=amount
		res_d.save()


###################### TRANSACIONS #####################
########################################################
#######################  DEPOSIT  ######################

async def set_deposit(uid,transid,currency,amount,date,status):
	with dbase:
		Udeposit.create(owner=uid,trans_id=transid,currency=currency,amount=amount,date=date,status=status)



async def set_deposit_status(uid,transid,status):
	with dbase:
		res = Udeposit.select().join(User).where(User.user_id==uid,Udeposit.trans_id==transid).get()
		res.status=status
		res.save()

###################### TRANSACIONS #####################
########################################################
#######################  WITHDRAW  #####################


async def set_withdraw(uid,transid,currency,amount,date,status):
	with dbase:
		Uwithdraw.create(owner=uid,trans_id=transid,currency=currency,amount=amount,date=date,status=status)




######################### BETS #########################

async def set_user_bet(race,uid,bet_value,bet_horse):
	with dbase:
		Bet.create(bet_id=race,user_id=uid,user_bet_value=bet_value,user_bet_horse=bet_horse)


# async def calculate(betid,position,booster):
# 	with dbase:
# 		Bet.update(user_bet_value=Bet.user_bet_value*booster,bet_status=1).where(Bet.bet_id==betid,Bet.user_bet_horse==position).execute()


async def calculate2(win1,win2,win3,betid):
	with dbase.atomic():
		boost =1.65
		for i in[win1,win2,win3]:
			boost-=0.2
			Bet.update(user_bet_value=Bet.user_bet_value*boost,bet_status=1).where(Bet.bet_id==betid,Bet.user_bet_horse==i).execute()


async def get_winners():
	with dbase.atomic():
		for res in Bet.select(Bet.user_id,Bet.user_bet_value).where(Bet.bet_status==1):
			res_w = Ubalance.select().join(User).where(User.user_id==res.user_id,Ubalance.marker==1).get()
			res_w.amount+=res.user_bet_value
			res_w.save()
		Bet.update(bet_status=2).where(Bet.bet_status==1).execute()


##########################################################
#ПЕРЕДЕЛАТЬ СТАТУС
			
		

######################### RACE #########################


async def race_create():
	with dbase:
		Race.create(jumper=1)
		return Race.select().where(Race.jumper==1).order_by(Race.race_id.desc()).limit(1)[0].race_id


async def race_close():
	with dbase:
		Race.update(jumper=0).where(Race.jumper==1).execute()


async def check_jumper():
	with dbase:
		return Race.select(Race.jumper).order_by(Race.race_id.desc()).limit(1)[0].jumper


async def get_current_race():
	with dbase:
		return Race.select(Race.race_id).order_by(Race.race_id.desc()).limit(1)[0].race_id


async def get_race_result(w1, w2, w3):
	with dbase:
		Race.update(win1=w1,win2=w2,win3=w3).where(Race.jumper == 1).execute()











