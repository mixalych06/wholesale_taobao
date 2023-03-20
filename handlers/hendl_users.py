from create_bot import bot, db
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputFile

from keyboards.kb_user import keyboard_user
from keyboards.kb_other import gen_markup_category


async def command_start(message: types.Message):
    await bot.send_photo(message.from_user.id, photo=InputFile('data/logo1.png'),
                         caption=f'<b>Привет, {message.from_user.first_name}!</b>\n'
                                 f'Для просмотра товара нажмите на кнопуку В наличии\n'
                                 f'<i>С предложениями и вопросами обращаться к\n'
                                 f'<a href="https://t.me/mixalych06">администратору</a></i>',
                         parse_mode='HTML', reply_markup=keyboard_user)


async def command_help(message: types.Message):
    await bot.send_photo(message.from_user.id, photo=InputFile('data/logo1.png'),
                         caption=f'<b>Привет, {message.from_user.first_name}!</b>\n'
                                 f'Для просмотра товара нажмите на кнопуку В наличии\n'
                                 f'<i>С предложениями и вопросами обращаться к\n'
                                 f'<a href="https://t.me/mixalych06">администратору</a></i>',
                         parse_mode='HTML', reply_markup=keyboard_user)


async def coutry(message: types.Message):
    """Кнопка товары в наличии"""
    countries = db.bd_checks_for_country_in_stock()
    country_dict = {country: 'categor_for_user' for country in countries}
    if countries:
        await bot.send_message(message.from_user.id, text='Выберите страну',
                               reply_markup=await gen_markup_category(country_dict))
        await message.delete()


async def categories_in_stock(callback_query: types.CallbackQuery):
    """Кнопки категория для user"""
    inline_command = callback_query.data.split(':')
    categories = db.bd_checks_for_category_in_stock(inline_command[1])
    categories_dict = {category: f'product_for_user:{inline_command[1]}' for category in categories}
    await callback_query.message.edit_text('Выберите категорию',
                                           reply_markup=await gen_markup_category(categories_dict))


async def product_in_stock_for_user(callback_query: types.CallbackQuery):
    inline_command = callback_query.data.split(':')
    product_for_user = db.bd_checks_for_category_product_in_stock(inline_command[1], inline_command[2])
    print(product_for_user)
    for i in product_for_user:
        await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id, photo=i[3],
                                            caption=f"<b>{i[4].strip().upper()}</b>\n{i[5]}\n<b>Цена: </b>{i[6]}",
                                                    parse_mode='HTML'
                                            )


def register_handler_users(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_help, text=['🆘Помощь'])
    dp.register_message_handler(coutry, text='Товары в наличии')
    dp.register_callback_query_handler(categories_in_stock, lambda x: x.data.startswith('categor_for_user'))
    dp.register_callback_query_handler(product_in_stock_for_user,
                                       lambda x: x.data.startswith('product_for_user'))
