from aiogram.utils import executor
from aiogram import types
from create_bot import dp
from handlers.hendl_users import register_handler_users
from handlers.hendl_admin import register_handler_admin

register_handler_admin(dp)
register_handler_users(dp)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
