from create_bot import bot, db
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputFile
from keyboards.kb_other import gen_markup_category
from aiogram.utils.exceptions import BadRequest
from keyboards.kb_edit_product import repl_for_categor_for_admin


async def coutry_for_admin(message: types.Message):
    """Кнопка товары в наличии"""
    countries = set(db.bd_checks_for_country_in_stock_for_admin())
    country_dict = {country: 'catforad' for country in countries}
    await bot.delete_message(message.chat.id, message.message_id)
    if countries:
        await bot.send_message(message.from_user.id, text='Выберите страну',
                               reply_markup=await gen_markup_category(country_dict))
    else:
        await bot.send_message(message.from_user.id, text=f'Нет товаров',
                               parse_mode='HTML')


async def categories_in_stock_for_admin(callback_query: types.CallbackQuery):
    """Кнопки категория для user"""
    inline_command = callback_query.data.split(':')
    user_id = callback_query.from_user.id
    categories = db.bd_checks_for_category_in_stock_for_admin(inline_command[1])
    categories_dict = {category: f'prodforad:{str(inline_command[1])}' for category in categories}
    try:
        await callback_query.message.edit_text(f'<b>{inline_command[1]}</b>\nВыберите категорию',
                                               reply_markup=await gen_markup_category(categories_dict),
                                               parse_mode='HTML')
    except BadRequest:
        await callback_query.message.delete()
        await bot.send_message(user_id, text=f'<b>{inline_command[1]}</b>\nВыберите категорию',
                               reply_markup=await gen_markup_category(categories_dict), parse_mode='HTML')


async def product_in_stock_for_admin(callback_query: types.CallbackQuery):
    """Выдаёт товары из выбраной категории"""
    inline_command = callback_query.data.split(':')
    number = 0
    product_for_user = db.bd_checks_for_category_product_in_stock_for_admin(inline_command[1], inline_command[2])
    print(product_for_user)
    user_caption = f'<b>{product_for_user[number][4].strip().upper()}</b>\n' \
                   f'<i>(В наличии {product_for_user[number][7]} шт.)</i>\n' \
                   f'{product_for_user[number][5]}\n<b>Цена: </b>{product_for_user[number][6]} руб.'
    await callback_query.message.delete()
    if len(product_for_user) > 1:
        await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id, photo=product_for_user[number][3],
                                            caption=user_caption, parse_mode='HTML',
                                            reply_markup=InlineKeyboardMarkup(row_width=4).add(
                                                InlineKeyboardButton("➕",
                                                                     callback_data=f'plus:'
                                                                                   f'{product_for_user[number][0]}:'
                                                                                   f'{len(product_for_user)}:'
                                                                                   f'{number}:{-1}'),
                                                InlineKeyboardButton("➖",
                                                                     callback_data=f'plus:'
                                                                                   f'{product_for_user[number][0]}:'
                                                                                   f'{len(product_for_user)}:'
                                                                                   f'{number}:{1}')
                                            )
                                            .add(
                                                InlineKeyboardButton("⬅️⬅️⬅️",
                                                                     callback_data=f'next_a:{inline_command[1]}:'
                                                                                   f'{inline_command[2]}:'
                                                                                   f'{len(product_for_user) - 1}'),
                                                InlineKeyboardButton(f'{number + 1}/{len(product_for_user)}',
                                                                     callback_data='null'),
                                                InlineKeyboardButton(
                                                    "➡️➡️➡️", callback_data=f'next_a:{inline_command[1]}:'
                                                                            f'{inline_command[2]}:{number + 1}')).add(
                                                InlineKeyboardButton('Удалить',
                                                                     callback_data=f'delprod:'
                                                                                   f'{product_for_user[number][0]}'),
                                                InlineKeyboardButton('Назад',
                                                                     callback_data=f'catforad:'
                                                                                   f'{product_for_user[number][1]}')))
    elif len(product_for_user) == 1:
        await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id, photo=product_for_user[number][3],
                                            caption=user_caption, parse_mode='HTML',
                                            reply_markup=InlineKeyboardMarkup(row_width=4).add(
                                                InlineKeyboardButton("➕",
                                                                     callback_data=f'plus:'
                                                                                   f'{product_for_user[number][0]}:'
                                                                                   f'{len(product_for_user)}:'
                                                                                   f'{number}:{-1}'),
                                                InlineKeyboardButton("➖",
                                                                     callback_data=f'plus:'
                                                                                   f'{product_for_user[number][0]}:'
                                                                                   f'{len(product_for_user)}:'
                                                                                   f'{number}:{1}')
                                            )
                                            .add(
                                                InlineKeyboardButton('⬅️⬅️⬅️',
                                                                     callback_data='null'),
                                                InlineKeyboardButton(f'{number + 1}/{len(product_for_user)}',
                                                                     callback_data='null'),
                                                InlineKeyboardButton('➡️➡️➡️',
                                                                     callback_data='null')).add(
                                                InlineKeyboardButton('Удалить',
                                                                     callback_data=f'delprod:'
                                                                                   f'{product_for_user[number][0]}'),
                                                InlineKeyboardButton('Назад',
                                                                     callback_data=f'catforad:'
                                                                                   f'{product_for_user[number][1]}')))


async def next_product_for_admin(callback_query: types.CallbackQuery):
    """Обработка кнопок пагинации"""
    inline_command = callback_query.data.split(':')
    number = int(inline_command[3])
    product_for_user = db.bd_checks_for_category_product_in_stock_for_admin(inline_command[1], inline_command[2])
    if len(product_for_user) > 1:
        try:
            user_caption = f'<b>{product_for_user[number][4].strip().upper()}</b>\n' \
                           f'<i>(В наличии {product_for_user[number][7]} шт.)</i>\n' \
                           f'{product_for_user[number][5]}\n<b>Цена: </b>{product_for_user[number][6]} руб.'
        except IndexError:
            number = len(product_for_user)
            user_caption = f'<b>{product_for_user[number][4].strip().upper()}</b>\n' \
                           f'<i>(В наличии {product_for_user[number][7]} шт.)</i>\n' \
                           f'{product_for_user[number][5]}\n<b>Цена: </b>{product_for_user[number][6]} руб.'
        photo = InputMediaPhoto(media=product_for_user[number][3], caption=user_caption, parse_mode='HTML')
        await callback_query.bot.edit_message_media(media=photo, chat_id=callback_query.message.chat.id,
                                                    message_id=callback_query.message.message_id,
                                                    reply_markup=await repl_for_categor_for_admin(len(product_for_user),
                                                                                                  product_for_user[number][
                                                                                                      0],
                                                                                                  inline_command[2],
                                                                                                  country=
                                                                                                  product_for_user[number][
                                                                                                      1],
                                                                                                  number=number))
    elif len(product_for_user) == 1:
        number = 0
        await callback_query.message.delete()
        user_caption = f'<b>{product_for_user[number][4].strip().upper()}</b>\n' \
                       f'<i>(В наличии {product_for_user[number][7]} шт.)</i>\n' \
                       f'{product_for_user[number][5]}\n<b>Цена: </b>{product_for_user[number][6]} руб.'
        await callback_query.bot.send_photo(chat_id=callback_query.message.chat.id, photo=product_for_user[number][3],
                                            caption=user_caption, parse_mode='HTML',
                                            reply_markup=InlineKeyboardMarkup(row_width=4).add(
                                                InlineKeyboardButton("➕",
                                                                     callback_data=f'plus:'
                                                                                   f'{product_for_user[number][0]}:'
                                                                                   f'{len(product_for_user)}:'
                                                                                   f'{number}:{-1}'),
                                                InlineKeyboardButton("➖",
                                                                     callback_data=f'plus:'
                                                                                   f'{product_for_user[number][0]}:'
                                                                                   f'{len(product_for_user)}:'
                                                                                   f'{number}:{1}')
                                            )
                                            .add(
                                                InlineKeyboardButton('⬅️⬅️⬅️',
                                                                     callback_data='null'),
                                                InlineKeyboardButton(f'{number + 1}/{len(product_for_user)}',
                                                                     callback_data='null'),
                                                InlineKeyboardButton('➡️➡️➡️',
                                                                     callback_data='null')).add(
                                                InlineKeyboardButton('Удалить',
                                                                     callback_data=f'delprod:'
                                                                                   f'{product_for_user[number][0]}'),
                                                InlineKeyboardButton('Назад',
                                                                     callback_data=f'catforad:'
                                                                                   f'{product_for_user[number][1]}')))
    else:
        await bot.send_message(callback_query.from_user.id, 'обнови')


async def del_prod(callback_query: types.CallbackQuery):
    inline_command = callback_query.data.split(':')
    print(inline_command)
    db.bd_del_prod(inline_command[1])


async def plus_prod(callback_query: types.CallbackQuery):
    inline_command = callback_query.data.split(':')
    lot = db.bd_returns_one_item(int(inline_command[1]))
    if lot[7] - int(inline_command[4]) >= 0:
        db.bd_changes_count_in_stock(int(inline_command[4]), int(inline_command[1]))
        await callback_query.message.edit_caption(caption=f'<b>{lot[4].strip().upper()}</b>\n'
                                                          f'<i>(В наличии {lot[7]-int(inline_command[4])} шт.)</i>\n'
                                                          f'{lot[5]}\n<b>Цена: </b>{lot[6]} руб.',
                                                  reply_markup=await repl_for_categor_for_admin(int(inline_command[2]),
                                                                                                inline_command[1],
                                                                                                lot[2],
                                                                                                country=lot[1],
                                                                                                number=int(inline_command[3])),
                                                  parse_mode='HTML')
        await callback_query.answer(text=f'{lot[4]}\nИзменено количество\n На складе {lot[7]-int(inline_command[4])} шт.')
    elif lot[7] - int(inline_command[4]) < 0:
        await callback_query.answer(text=f'{lot[4]}\nКоличество не может быль меньше 0')


def register_handler_edit_product(dp: Dispatcher):
    dp.register_message_handler(coutry_for_admin, text='Редактировать товары')

    dp.register_callback_query_handler(categories_in_stock_for_admin, lambda x: x.data.startswith('catforad'))
    dp.register_callback_query_handler(product_in_stock_for_admin, lambda x: x.data.startswith('prodforad'))
    dp.register_callback_query_handler(next_product_for_admin, lambda x: x.data.startswith('next_a'))
    dp.register_callback_query_handler(del_prod, lambda x: x.data.startswith('delprod'))
    dp.register_callback_query_handler(plus_prod, lambda x: x.data.startswith('plus'))