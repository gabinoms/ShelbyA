from datas.bh_methods import usr_info

async def profile_info(uid,r0,r1,r2,r3,r4,r5):

#res[0] - Id 				#res[2] - label DEMO or CASH   res[4] - amount
#res[1] - first_name		#res[3] - token     		   res[5] - marker	         res[6] -VIP


	msg = f"""
🪪 <b>account</b>\t\t\t🟢 {r2}
<code>VIP</code> {r5}
{r1}
•
    Баланс
•  {'💵' if r2 =='DEMO' else r3}  <code><b>{r4}</b></code>
•
"""
	return msg


async def settings_info(uid,status):
	
# off ⚫️ # on 🟢	
	if status!='DEMO':
		led1='⚫️'
		led2='🟢'
	else:
		led2='⚫️'
		led1='🟢'

	msg = f"""
⚙️ настройки:

•   {led1} DEMO {led2} CAsH
•
•
•   <code>реф сслыка</code>
"""
	return msg

