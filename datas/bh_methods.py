from .bh_clases import dbase, GameMode, Race, Bet, Ubalance, Udeposit, Uwithdraw, User, Referral, Vip
from config import referral_link


######################## ADMIN #########################

async def players_count():
	with dbase:
		return User.select().count()

async def max_user_balance():
	rbal=''
	with dbase:
		res = Ubalance.select().join(User).where(Ubalance.token!='DEMO').order_by(Ubalance.amount.desc()).limit(3)
		for r in res:
			#if r.token!='DEMO':
			rbal+=f'<code>{r.owner.user_id}</code>: <b>{r.amount} {r.token}</b>\n'
	return rbal




async def set_silent(silent_mode):
	with dbase:
		res = GameMode.select().where(GameMode.mode_parameter=='Silent').get()
		res.mode_position=silent_mode
		res.mode_count=0
		res.save()

async def get_silent():
	with dbase:
		res = GameMode.select().where(GameMode.mode_parameter=='Silent').get()
		return res.mode_position

async def get_silent_word_count(wordcount=0):
	with dbase:
		res = GameMode.select().where(GameMode.mode_parameter=='Silent').get()
		res.mode_count+=wordcount
		res.save()
		return res.mode_count


async def get_race_without_bets(racecount=0):
	with dbase:
		res = GameMode.select().where(GameMode.mode_parameter=='Silent').get()
		res.mode_count_stop+=racecount
		res.save()
		return res.mode_count_stop

######################### USER #########################

async def usr_exists(uid):
	with dbase:
		try:
			res = User.select().where(User.user_id == uid).get()
		except User.DoesNotExist:
			res = None
	return res


async def usr_add(uid, uname, rfid, rlink, datereg):
	with dbase.atomic():
		data = [(uid,'DEMO',1000,1),
				(uid,'TON',0,2),
				(uid,'VIRUS',0,2),
				(uid,'KISS',0,2),
				(uid,'IVS',0,2),
				(uid,'****',0,2)]
		

		User.create(user_id=uid, user_name=uname, user_ref_link=rlink )
		Ubalance.insert_many(data, fields=[Ubalance.owner,Ubalance.token,Ubalance.amount,Ubalance.marker]).execute()
		Referral.insert(owner=uid, ref_id=rfid, registration_date=datereg).execute()
		Vip.insert(owner=uid).execute()
		


async def usr_info(uid):
	ub_all = ''
	with dbase:
		res = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.marker==1).get()
		if res.owner.label=='DEMO':
			amount_ed = format(res.amount, '.2f')
			ub_all = f'💵 : {amount_ed}\n'

			#return res.owner.user_id, res.owner.user_name, res.owner.label, ub_all, res.owner.user_vip_status

		elif res.owner.label=='CAsH':
			
			res1 = Ubalance.select().join(User).where(User.user_id==uid, Ubalance.token!='DEMO', Ubalance.token!='****')

			for r1 in res1:
				amount_ed = format(r1.amount, '.2f')
				if r1.marker==1:
					ub_all+=f'🟢<b>{r1.token}</b> : <code>{amount_ed}</code>\n'
				else:
					ub_all+=f'⚫️<b>{r1.token}</b> : <code>{amount_ed}</code>\n'

		name_uid = f'{res.owner.user_id}\t\t\t\t{res.owner.user_name}'
		

		return name_uid, res.owner.label, ub_all
			



async def usr_info_all(uid):
	if await usr_exists(uid)!=None:
		ub_all=''#all user balances
		with dbase:
			res = Ubalance.select().join(User).where(User.user_id==uid, Ubalance.token!='DEMO')
			for r1 in res:
				ub_all+=f"{r1.token}: {r1.amount}\n"
			return r1.owner.user_id, r1.owner.user_name, ub_all
	else:

		return 'ne','ne','ne'




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

async def get_active_wallets(uid):#for admin panel:info about user
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

######################### VIP #########################


async def check_vip_status(uid):
	with dbase:
		res = Vip.select().join(User).where(User.user_id==uid).get()
		return res.vip_status


async def check_vip_info(uid):
	with dbase:
		vipst=[]
		res = Vip.select().join(User).where(User.user_id==uid).get()
		vipst.append(res.vip_status)
		vipst.append(res.vip_status_time)
		vipst.append(res.vip_points)
		vipst.append(res.vip_daily_bonus)

		return vipst

async def check_daily_timer(uid):
	with dbase:
		res = Vip.select().join(User).where(User.user_id==uid).get()
		return res.vip_daily_bonus

async def zero_timer(uid):
	with dbase:
		res = Vip.select().join(User).where(User.user_id==uid).get()
		res.vip_daily_bonus=0
		res.save()

async def add_vp(uid, amount, daily_timer=0):#add vp by gift button
	with dbase:
		res = Vip.select().join(User).where(User.user_id==uid).get()
		res.vip_points+=amount
		res.vip_daily_bonus = daily_timer
		res.save()


async def ref_count(uid):
	with dbase:
		res = Referral.select().where(Referral.ref_id==uid).count()
		return res

######################### CASH #########################

async def check_balance(uid):
	with dbase:
		res = Ubalance.select().join(User).where(User.user_id == uid,Ubalance.marker==1).get()
		return res.amount, res.token


async def check_balance_selected(uid,label):
	with dbase:
		res = Ubalance.select().join(User).where(User.user_id==uid,Ubalance.token==label.upper()).get()
		amount_ed = format(res.amount, '.2f')
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

async def withdraw_pending(uid,transid,token,amount,date,status='Pending'):
	with dbase:
		Uwithdraw.create(owner=uid,trans_id=transid,currency=token,amount=amount,date=date,status=status)


async def withdraw_pending_remove(transid,status):
	with dbase:
		res = Uwithdraw.select().where(Uwithdraw.trans_id==transid).get()
		res.status=status
		res.save()


async def withdraw_decline(transid):
	with dbase:
		res = Uwithdraw.select().join(User).where(Uwithdraw.trans_id==transid, Uwithdraw.status=='Pending').get()
		res.status = 'Decline'
		res.save()


async def get_withdraw_details(transid):
	with dbase:
		res = Uwithdraw.select().join(User).where(Uwithdraw.trans_id==transid).get()
		return res.owner.user_id, res.currency, res.amount, res.status



async def set_withdraw(uid,transid,currency,amount,date,status):
	with dbase:
		Uwithdraw.create(owner=uid,trans_id=transid,currency=currency,amount=amount,date=date,status=status)




######################### BETS #########################

async def set_user_bet(race,uid,bet_value,bet_horse):
	r_bonus = (await ref_count(uid))/100
	if r_bonus > 0.1:
		r_bonus=0.1
	with dbase:
		Bet.create(bet_id=race,user_id=uid,user_bet_value=bet_value+r_bonus,user_bet_horse=bet_horse)
		res = Vip.select().join(User).where(User.user_id==uid).get()
		res.vip_points+=0.1
		res.save()


# async def calculate(betid,position,booster):
# 	with dbase:
# 		Bet.update(user_bet_value=Bet.user_bet_value*booster,bet_status=1).where(Bet.bet_id==betid,Bet.user_bet_horse==position).execute()

async def calculate_bets(current_race):
	with dbase:
		return Bet.select().where(Bet.bet_id==current_race).count()

async def calculate2(win1,win2,win3,betid):
	with dbase.atomic():
		boost =1.65
		for i in[win1,win2,win3]:
			boost-=0.2
			Bet.update(user_bet_value=Bet.user_bet_value*boost,bet_status=1).where(Bet.bet_id==betid,Bet.user_bet_horse==i).execute()


async def get_winners():

	winners=set()
	with dbase.atomic():
		for res in Bet.select(Bet.user_id,Bet.user_bet_value).where(Bet.bet_status==1):
			res_w = Ubalance.select().join(User).where(User.user_id==res.user_id,Ubalance.marker==1).get()
			res_w.amount+=res.user_bet_value
			res_w.save()
			winners.add(res_w.owner.user_name)
		Bet.update(bet_status=2).where(Bet.bet_status==1).execute()
		return winners


##########################################################

			
		

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