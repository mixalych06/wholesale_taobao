from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv(filename='.env'), encoding="utf-8", override=True)
TOKEN = os.environ.get('TOKENTEST')
CHAT_ID = os.environ.get('CHAT_ID')
ADMIN_ID = os.environ.get('ADMIN_ID')

bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher(bot, storage=MemoryStorage())
