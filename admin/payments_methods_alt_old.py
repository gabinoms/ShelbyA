import requests

from engine import rocketpay_key


async def get_min_dep(val):
	headers = {'accept': 'application/json',}

	res = requests.get('https://pay.ton-rocket.com/currencies/available', headers=headers).json()
	for i in res['data']['results']:
		if i['name'] == val:
			return i['minInvoice']



			

async def get_min_with(val):
	headers = {'accept': 'application/json',}

	res = requests.get('https://pay.ton-rocket.com/currencies/available', headers=headers).json()
	for i in res['data']['results']:
		if i['name'] == val:
			return i['minCheque']



async def get_main_balance(val=None):#by one currency
	headers = {'accept': 'application/json', 'Rocket-Pay-Key': rocketpay_key,}

	res = requests.get('https://pay.ton-rocket.com/app/info', headers=headers).json()
	if val==None:
		res1 = ''
		for i in res['data']['balances']:
			if i['balance']!=0.0:
				res1+=f"{i['currency']}: {i['balance']}\n"

		return res1

	else:
		for i in res['data']['balances']:
			if i['currency'] == val:
				return i['balance']



async def dep_create(val, amnt):
	headers = {'accept': 'application/json', 'Rocket-Pay-Key': rocketpay_key, 'Content-Type': 'application/json',}
	json_data ={
	'amount': 0,
	'minPayment': amnt,
	'numPayments': 0,
	'currency': val,
	'description': 'GHС',
	'hiddenMessage': 'GoldenHorseClub желает вам хорошего настроения и приятного отдыха',
	'callbackUrl': 'https://t.me/ton_rocket',
	'payload': ' ',
	'expiredIn': 60,
	}

	res = requests.post('https://pay.ton-rocket.com/tg-invoices', headers=headers, json=json_data).json()
	return res['data']['id'], res['data']['link']



async def dep_status_check(dep_id):
	headers = {'accept': 'application/json', 'Rocket-Pay-Key': rocketpay_key,}
	res = requests.get(f'https://pay.ton-rocket.com/tg-invoices/{dep_id}', headers=headers).json()
	return res




async def with_create(uid, trid, val, amnt):
	headers = {'accept': 'application/json', 'Rocket-Pay-Key': rocketpay_key, 'Content-Type': 'application/json',}
	json_data = {
	'tgUserId': uid,
	'currency': val,
	'amount': amnt,
	'transferId': trid,
	'description': 'GoldenHorseClub желает вам хорошего настроения и приятного отдыха',
	}

	res = requests.post('https://pay.ton-rocket.com/app/transfer', headers=headers, json=json_data).json()
	return res



async def with_status():
	pass
#################################################################################################################
#																												#	
#################################################################################################################

