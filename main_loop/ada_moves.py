from engine import bot, scheduler
from config import CHAT
from datas.bh_methods import get_silent_word_count, get_race_without_bets

async def letsplay():
	if scheduler.state==0:
		scheduler.start()
		await bot.send_message(CHAT,'🙃 давайте поиграем... я сейчас все подготовлю, а вы пока почитайте <a href="https://t.me/GHC_chan">правила</a>',disable_web_page_preview=True)
	elif scheduler.state==2:
		scheduler.resume()
		await bot.send_message(CHAT,'🙃 дамы и господа, занимайте места... скоро начнется новый заезд.\n<a href="https://t.me/GHC_chan">правила</a>',disable_web_page_preview=True)



async def stopgame():
	race_count = await get_race_without_bets()

	if race_count<5:
		await get_race_without_bets(1)
	else:
		scheduler.pause()
		await bot.send_message(CHAT,'предлагаю взять паузу...кстати, в баре есть холодные напитки 🙃')
		await get_silent_word_count(-3)
		await get_race_without_bets(-5)