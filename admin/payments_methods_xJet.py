from xjet import JetAPI
from xjet.constants import xJetNet

from engine import api_key, private_key

api = JetAPI(
    api_key=api_key,
    private_key=private_key,
    network='mainnet' # or xJetNet.MAINNET
)


# await api.invoice_create(currency, amount, description, max_payments) # create invoice
# await api.invoice_status(invoice_status) # get invoice status
# await api.invoice_list() # get invoices on account

async def dep_create(val,amnt):
	res = await api.invoice_create(val, amnt) # create invoice
	return res['invoice_id'], res['external_link']

async def dep_status_check(id_d):
	return await api.invoice_status(id_d)


async def get_main_balance(val=None):
	res = await api.balance()
	for i in range(len(res['balances'])):
		if res['balances'][i]['currency'] == val:
			return res['balances'][i]['amount']


async def with_create(val,amnt):
	res = await api.cheque_create(val, amnt)
	print (res['cheque_id'])
	return res['cheque_id'],res['external_link']

async def with_status(id_w):
	res = await api.cheque_status(id_w)
	return res['status']

# 	CHECK {'cheque_id': '63e5242d28c9d325b3ba42af', 'external_link': 'https://t.me/xJetSwapBot?start=c_63e5242d28c9d325b3ba4
# 2af'}