from create_bot import bot, db
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputFile

async def command_help(message: types.Message):
    await bot.send_photo(message.from_user.id, photo=InputFile('data/logo1.png'),
                         caption=f'<b>Привет, {message.from_user.first_name}!</b>\n'
                                 f'Для просмотра товара нажмите на кнопуку В наличии\n'
                                 f'<i>С предложениями и вопросами обращаться к\n'
                                 f'<a href="https://t.me/mixalych06">администратору</a></i>',
                         parse_mode='HTML', reply_markup=keyboard_user)

def register_handler_order(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])