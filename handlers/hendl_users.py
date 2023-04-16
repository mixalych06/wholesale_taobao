from create_bot import bot, db
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputFile
from aiogram.utils.exceptions import BadRequest
from keyboards.kb_user import keyboard_user, repl_for_categor
from keyboards.kb_other import gen_markup_category
from datetime import date


async def command_start(message: types.Message):
    if db.bd_checks_the_existence_of_the_user(message.from_user.id):
        await bot.send_photo(message.from_user.id, photo=InputFile('data/logo1.png'),
                             caption=f'<b>Привет, {message.from_user.first_name}!</b>\n'
                                     f'Для просмотра товара нажмите на кнопуку В наличии\n'
                                     f'<i>С предложениями и вопросами обращаться к\n'
                                     f'<a href="https://t.me/mixalych06">администратору</a></i>',
                             parse_mode='HTML', reply_markup=keyboard_user)
    else:
        db.bd_add_new_user(message.from_user.id, message.from_user.first_name, date.today())
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


async def categories_in_stock(callback_query: types.CallbackQuery):
    """Кнопки категория для user"""
    inline_command = callback_query.data.split(':')
    user_id = callback_query.from_user.id
    categories = db.bd_checks_for_category_in_stock(inline_command[1])
    categories_dict = {category: f'product_for_user:{inline_command[1]}' for category in categories}
    try:
        await callback_query.message.edit_text('Выберите категорию',
                                               reply_markup=await gen_markup_category(categories_dict))
    except BadRequest:
        await callback_query.message.delete()
        await bot.send_message(user_id, text='Выберите категорию',
                               reply_markup=await gen_markup_category(categories_dict))


async def product_in_stock_for_user(callback_query: types.CallbackQuery):
    """Выдаёт товары из выбраной категории"""
    inline_command = callback_query.data.split(':')
    print(inline_command)
    number = 0
    product_for_user = db.bd_checks_for_category_product_in_stock(inline_command[1], inline_command[2])
    print(product_for_user)
    user_caption = f'<b>{product_for_user[number][4].strip().upper()}</b>\n' \
                   f'<i>(В наличии {product_for_user[number][7]} шт.)</i>\n' \
                   f'{product_for_user[number][5]}\n<b>Цена: </b>{product_for_user[number][6]} руб.'
    await callback_query.message.delete()
    print(product_for_user[number][1])
    if len(product_for_user) > 1:
        await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id, photo=product_for_user[number][3],
                                            caption=user_caption, parse_mode='HTML',
                                            reply_markup=InlineKeyboardMarkup(row_width=4).add(
                                                InlineKeyboardButton(f'{number + 1}/{len(product_for_user)}',
                                                                     callback_data='null')).add(
                                                InlineKeyboardButton("⬅️⬅️⬅️",
                                                                     callback_data=f'next_u:{inline_command[1]}:'
                                                                                   f'{inline_command[2]}:'
                                                                                   f'{len(product_for_user) - 1}'),
                                                InlineKeyboardButton(
                                                    "➡️➡️➡️", callback_data=f'next_u:{inline_command[1]}:'
                                                                            f'{inline_command[2]}:{number + 1}')).add(
                                                InlineKeyboardButton('В корзину',
                                                                     callback_data=f'add_basket:'
                                                                                   f'{product_for_user[number][0]}'),
                                                InlineKeyboardButton('Назад',
                                                                     callback_data=f'categor_for_user:'
                                                                                   f'{product_for_user[number][1]}')))
    elif len(product_for_user) == 1:
        await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id, photo=product_for_user[number][3],
                                            caption=user_caption, parse_mode='HTML',
                                            reply_markup=InlineKeyboardMarkup(row_width=4).add(
                                                InlineKeyboardButton(f'{number + 1}/{len(product_for_user)}',
                                                                     callback_data='null')).add(
                                                InlineKeyboardButton('⬅️⬅️⬅️',
                                                                     callback_data='null'),
                                                InlineKeyboardButton('➡️➡️➡️',
                                                                     callback_data='null')).add(
                                                InlineKeyboardButton('В корзину',
                                                                     callback_data=f'add_basket:'
                                                                                   f'{product_for_user[number][0]}'),
                                                InlineKeyboardButton('Назад',
                                                                     callback_data=f'categor_for_user:'
                                                                                   f'{product_for_user[number][1]}')))


async def next_product_user(callback_query: types.CallbackQuery):
    """Обработка кнопок пагинации"""
    inline_command = callback_query.data.split(':')
    number = int(inline_command[3])
    product_for_user = db.bd_checks_for_category_product_in_stock(inline_command[1], inline_command[2])
    user_caption = f'<b>{product_for_user[number][4].strip().upper()}</b>\n' \
                   f'<i>(В наличии {product_for_user[number][7]} шт.)</i>\n' \
                   f'{product_for_user[number][5]}\n<b>Цена: </b>{product_for_user[number][6]} руб.'
    photo = InputMediaPhoto(media=product_for_user[number][3], caption=user_caption, parse_mode='HTML')
    await callback_query.bot.edit_message_media(media=photo, chat_id=callback_query.message.chat.id,
                                                message_id=callback_query.message.message_id,
                                                reply_markup=await repl_for_categor(len(product_for_user),
                                                                                    product_for_user[number][0],
                                                                                    inline_command[1],
                                                                                    inline_command[2],
                                                                                    number))


async def user_add_product_to_the_basket(callback_query: types.CallbackQuery):
    """пользователь добавляет товар в корзину"""
    inline_command = callback_query.data.split(':')
    how_many_products = db.bd_returns_one_item(inline_command[1])[7]
    lot = db.bd_checks_product_in_the_basket(callback_query.from_user.id, inline_command[1])
    print(lot)
    print('11', how_many_products)
    if not lot:
        db.bd_add_product_in_basket(callback_query.from_user.id, inline_command[1])
        await callback_query.answer(text=f'Добавлено в корзину\nВ корзине 1 шт.', cache_time=1)
        return
    elif int(lot[0][0]) >= int(how_many_products):
        await callback_query.answer(text=f'Больше нельзя добавить\nВ корзине {lot[0][0]} шт.', cache_time=1)
        return
    else:
        db.bd_add_product_in_basket(callback_query.from_user.id, inline_command[1])
        await callback_query.answer(text=f'Добавлено в корзину\nВ корзине {lot[0][0]+1} шт.', cache_time=1)


def register_handler_users(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_help, text=['🆘Помощь'])
    dp.register_message_handler(coutry, text='Товары в наличии')
    dp.register_callback_query_handler(categories_in_stock, lambda x: x.data.startswith('categor_for_user'))
    dp.register_callback_query_handler(product_in_stock_for_user,
                                       lambda x: x.data.startswith('product_for_user'))
    dp.register_callback_query_handler(next_product_user, lambda x: x.data.startswith('next_u'))
    dp.register_callback_query_handler(user_add_product_to_the_basket, lambda x: x.data.startswith('add_basket'))
