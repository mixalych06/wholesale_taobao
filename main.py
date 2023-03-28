from aiogram.utils import executor
from aiogram import types
from create_bot import dp
from handlers.hendl_users import register_handler_users
from handlers.hendl_admin import register_handler_admin
from handlers.hendl_other import register_handler_other
from handlers.hendl_basket import register_handler_basket

register_handler_admin(dp)
register_handler_users(dp)
register_handler_other(dp)
register_handler_basket(dp)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
