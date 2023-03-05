from datas.bh_methods import usr_info, ref_count, check_vip_info
from users.referrals.ref_methods import encoder
from config import referral_link


#res[0] - name + Id   #res[2] - balances   
#res[1] - label		  

async def profile_info(r0,r1,r2):
	refs = r0.split('\t\t\t\t')[0]# uid
	uname = r0.split('\t\t\t\t')[1]#uname
	vip = await check_vip_info(refs)


	msg = f"""
🪪 <code>{refs}</code>\t\t\t🟢 {r1}
{uname}\t\t\t\t\t\t\t\t<b>VIP</b> : {vip[0]}
<b>vp</b> : {vip[2]}
•
    Баланс
{r2}
•
Рефералы : {await ref_count(refs)}
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
•   <i>ваша реферальная сслыка</i>
<code>{referral_link+(await encoder(uid))}</code>
"""
	return msg

