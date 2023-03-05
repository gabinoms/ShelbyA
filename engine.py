from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.utils.callback_data import CallbackData


import os
from dotenv import load_dotenv, find_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

cbd_cash = CallbackData('pref', 'but', 'value')
cbd_cash1 = CallbackData('cash', 'jump', 'but', 'value')

cbd_adm = CallbackData('adm','but','value')


load_dotenv(find_dotenv())
# api_key = os.getenv('JAPIKEY')
# private_key = os.getenv('JAPITOKEN')
rocketpay_key = os.getenv('ROCKETPAY')
webh_url = os.getenv('WH_URL')
bot = Bot(os.getenv('TOKEN'), parse_mode='HTML')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()

