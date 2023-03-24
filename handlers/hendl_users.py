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
    """Выдаёт товары из выбраной категории"""
    inline_command = callback_query.data.split(':')
    number = 0
    product_for_user = db.bd_checks_for_category_product_in_stock(inline_command[1], inline_command[2])
    print(product_for_user[number])
    user_caption = f"<b>{product_for_user[number][4].strip().upper()}</b>\n" \
                   f"{product_for_user[number][5]}\n<b>Цена: </b>{product_for_user[number][6]}"
    if len(product_for_user) > 1:
        await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id, photo=product_for_user[number][3],
                                            caption=user_caption,
                                            parse_mode='HTML',
                                            reply_markup=InlineKeyboardMarkup(row_width=4).
                                            add(InlineKeyboardButton(f'{number + 1}/{len(product_for_user)}',
                                                                     callback_data='null')).
                                            add(InlineKeyboardButton("⬅️⬅️⬅️",
                                                                     callback_data=f"next_u:{inline_command[1]}:"
                                                                                   f"{inline_command[2]}:"
                                                                                   f"{len(product_for_user) - 1}"),
                                                InlineKeyboardButton("➡️➡️➡️",
                                                                     callback_data=f"next_u:{inline_command[1]}:"
                                                                                   f"{inline_command[2]}:{number + 1}")).
                                            add(InlineKeyboardButton('В корзину',
                                                                     callback_data=f"basket:"
                                                                                   f"{product_for_user[number][0]}")))
    elif len(product_for_user) == 1:
        await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id, photo=product_for_user[number][3],
                                            caption=user_caption,
                                            parse_mode='HTML',
                                            reply_markup=InlineKeyboardMarkup(row_width=4).
                                            add(InlineKeyboardButton(f'{number + 1}/{len(product_for_user)}',
                                                                     callback_data='null')).
                                            add(InlineKeyboardButton("⬅️⬅️⬅️",
                                                                     callback_data='null'),
                                                InlineKeyboardButton("➡️➡️➡️",
                                                                     callback_data='null')).
                                            add(InlineKeyboardButton('В корзину',
                                                                     callback_data=f"basket:"
                                                                                   f"{product_for_user[number][0]}")))


async def next_product_user(callback_query: types.CallbackQuery):
    """Обработка кнопок пагинации"""
    inline_command = callback_query.data.split(':')
    number = int(inline_command[3])
    product_for_user = db.bd_checks_for_category_product_in_stock(inline_command[1], inline_command[2])
    user_caption = f"<b>{product_for_user[number][4].strip().upper()}</b>\n" \
                   f"{product_for_user[number][5]}\n<b>Цена: </b>{product_for_user[number][6]}"
    photo = InputMediaPhoto(media=product_for_user[number][3], caption=user_caption, parse_mode='HTML')
    if 0 < number < len(product_for_user) - 1:
        await callback_query.bot.edit_message_media(media=photo, chat_id=callback_query.message.chat.id,
                                                    message_id=callback_query.message.message_id,
                                                    reply_markup=InlineKeyboardMarkup(row_width=4).
                                                    add(InlineKeyboardButton(f'{number + 1}/{len(product_for_user)}',
                                                                             callback_data='null')).
                                                    add(InlineKeyboardButton("⬅️⬅️⬅️",
                                                                             callback_data=f"next_u:{inline_command[1]}:"
                                                                                           f"{inline_command[2]}:"
                                                                                           f"{number - 1}"),
                                                        InlineKeyboardButton("➡️➡️➡️",
                                                                             callback_data=f"next_u:{inline_command[1]}:"
                                                                                           f"{inline_command[2]}:{number + 1}")).
                                                    add(InlineKeyboardButton('В корзину',
                                                                             callback_data=f"basket:"
                                                                                   f"{product_for_user[number][0]}")))
    elif number == 0:
        await callback_query.bot.edit_message_media(media=photo, chat_id=callback_query.message.chat.id,
                                                    message_id=callback_query.message.message_id,
                                                    reply_markup=InlineKeyboardMarkup(row_width=4).
                                                    add(InlineKeyboardButton(f'{number + 1}/{len(product_for_user)}',
                                                                             callback_data='null')).
                                                    add(InlineKeyboardButton("⬅️⬅️⬅️",
                                                                             callback_data=f"next_u:{inline_command[1]}:"
                                                                                           f"{inline_command[2]}:"
                                                                                           f"{len(product_for_user) - 1}"),
                                                        InlineKeyboardButton("➡️➡️➡️",
                                                                             callback_data=f"next_u:{inline_command[1]}:"
                                                                                           f"{inline_command[2]}:{number + 1}")).
                                                    add(InlineKeyboardButton('В корзину',
                                                                             callback_data=f"basket:"
                                                                                   f"{product_for_user[number][0]}")))
    elif number == len(product_for_user) - 1:
        await callback_query.bot.edit_message_media(media=photo, chat_id=callback_query.message.chat.id,
                                                    message_id=callback_query.message.message_id,
                                                    reply_markup=InlineKeyboardMarkup(row_width=4).
                                                    add(InlineKeyboardButton(f'{number + 1}/{len(product_for_user)}',
                                                                             callback_data='null')).
                                                    add(InlineKeyboardButton("⬅️⬅️⬅️",
                                                                             callback_data=f"next_u:{inline_command[1]}:"
                                                                                           f"{inline_command[2]}:"
                                                                                           f"{number - 1}"),
                                                        InlineKeyboardButton("➡️➡️➡️",
                                                                             callback_data=f"next_u:{inline_command[1]}:"
                                                                                           f"{inline_command[2]}:{0}")).
                                                    add(InlineKeyboardButton('В корзину',
                                                                             callback_data=f"basket:"
                                                                                   f"{product_for_user[number][0]}")))

def user_add_product_to_the_basket(callback_query: types.CallbackQuery):
    """пользователь добавляет товар в корзину"""
    inline_command = callback_query.data.split(':')
    number = int(inline_command[3])
    product_for_user = db.bd_checks_for_category_product_in_stock(inline_command[1], inline_command[2])
    user_caption = f"<b>{product_for_user[number][4].strip().upper()}</b>\n



def register_handler_users(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_help, text=['🆘Помощь'])
    dp.register_message_handler(coutry, text='Товары в наличии')
    dp.register_callback_query_handler(categories_in_stock, lambda x: x.data.startswith('categor_for_user'))
    dp.register_callback_query_handler(product_in_stock_for_user,
                                       lambda x: x.data.startswith('product_for_user'))
    dp.register_callback_query_handler(next_product_user, lambda x: x.data.startswith('next_u'))
    dp.register_callback_query_handler(user_add_product_to_the_basket, lambda x: x.data.startswith('basket'))
