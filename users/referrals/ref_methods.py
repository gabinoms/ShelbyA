import base64

from datas.bh_methods import usr_exists


async def encoder(to_ascii):# return ref_link from uid
	
	encoded = base64.b64encode(str(to_ascii).encode('ascii'))
	link = encoded.decode('ascii')
	return link


async def decoder(from_ascii):#return uid from ref_link
	decoded = base64.b64decode(from_ascii.encode('ascii'))
	return decoded.decode('ascii')


async def get_ref_link(uid, link):

	ref_link = await encoder(uid)
	try:
		get_uid = await decoder(link)
		is_valid_reflink = await usr_exists(get_uid)
		if is_valid_reflink == None or get_uid=='' or get_uid==str(uid):
			return 'refer', ref_link
		elif get_uid!='':
			return get_uid , ref_link


	except:
		return 'refer', ref_link