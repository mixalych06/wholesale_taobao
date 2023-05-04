from create_bot import bot, db
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from create_bot import ADMIN_ID
from datetime import datetime
from keyboards.kb_order import repl_for_order
from keyboards.kb_user import keyboard_user


async def buy_step1(callback_query: types.CallbackQuery):
    inline_command = callback_query.data.split(':')
    all_product = db.bd_all_product_for_user_in_the_basket(int(inline_command[1]))
    id_products = [id_prod[1] for id_prod in all_product]
    for i in all_product:
        prod = db.bd_returns_one_item(i[1])
        if not prod or not int(prod[7]) or not int(prod[-1]):
            db.bd_checking_availability(0, 0, callback_query.from_user.id, i[1])
            continue
        elif int(i[2]) <= int(prod[7]) and int(prod[-1]):  # если товаров в корзине меньше или равно чем в наличии
            db.bd_checking_availability(int(i[2]), 1, callback_query.from_user.id, i[1])
            continue
        elif int(i[2]) > int(prod[7]) and int(prod[-1]):
            db.bd_checking_availability(int(prod[7]), 1, callback_query.from_user.id, i[1])
    await buy_step2(callback_query.from_user.id)


async def buy_step2(user_id):
    """После проверки наличия отправляем заказ на сборку или отвечаем что товара нет или изменился"""
    all_user_prod = db.bd_all_product_for_user_in_the_basket(user_id)  # все товары пользователя в корзине
    user_prod = db.bd_product_for_user_in_the_basket_availability(
        user_id)  # товары пользователя в корзине которые есть в наличии
    all_count = [j[2] for j in all_user_prod if j[2] == j[3] and j[4] == 1]
    if not user_prod:
        await bot.send_message(user_id, text='Наличие товаров проверено, к сожалению, ни одного товара из '
                                             'корзины сейчас нет в наличии')
        db.bd_del_all_basket_from_user(user_id)
    elif len(all_user_prod) == len(all_count):
        await order_formation(user_id)
    elif len(all_user_prod) > len(all_count):
        await bot.send_message(user_id, text=f'В наличии не весь заказ\nИсправлено в соответствии с наличием')

        await order_confirmation(user_id)


async def order_confirmation(user_id):
    """Ожидание подтверждения заказа при недостаточном количестве в наличии на складе"""
    number = 0
    user_prod_basket = db.bd_product_for_user_in_the_basket_availability(user_id)
    user_prod = db.bd_returns_one_item(int(user_prod_basket[number][1]))
    if len(user_prod_basket) == 1:
        await bot.send_photo(user_id, photo=user_prod[3],
                             caption=f'<b>{user_prod[4].strip().upper()}</b>\n'
                                     f'{user_prod[5]}\n<b>Цена: </b>{user_prod[6]}',
                             reply_markup=InlineKeyboardMarkup().
                             add(InlineKeyboardButton(f'Заказ:{user_prod_basket[number][3]} шт.',
                                                      callback_data=f"null")).
                             add(InlineKeyboardButton('Купить', callback_data=f"yes_buy:{user_id}"),
                                 InlineKeyboardButton('Отмена', callback_data=f"no_buy:{user_id}")), parse_mode='HTML')
    elif len(user_prod_basket) > 1:
        await bot.send_photo(user_id, photo=user_prod[3],
                             caption=f'<b>{user_prod[4].strip().upper()}</b>\n'
                                     f'{user_prod[5]}\n<b>Цена: </b>{user_prod[6]}',
                             reply_markup=await repl_for_order(user_id, lot=user_prod_basket[number][3],
                                                               len_goods=len(user_prod_basket)), parse_mode='HTML')


async def next_order(callback_query: types.CallbackQuery):
    """Пагинация при исправленом заазе"""
    inline_command = callback_query.data.split(':')
    number = int(inline_command[1])
    user_prod_basket = db.bd_product_for_user_in_the_basket_availability(callback_query.from_user.id)
    user_prod = db.bd_returns_one_item(int(user_prod_basket[number][1]))
    user_caption = f'<b>{user_prod[4].strip().upper()}</b>\n{user_prod[5]}\n<b>Цена: </b>{user_prod[6]}'
    photo = InputMediaPhoto(media=user_prod[3], caption=user_caption, parse_mode='HTML')
    await callback_query.bot.edit_message_media(media=photo, chat_id=callback_query.message.chat.id,
                                                message_id=callback_query.message.message_id,
                                                reply_markup=await repl_for_order(callback_query.from_user.id,
                                                                                  number=number,
                                                                                  lot=user_prod_basket[number][3],
                                                                                  len_goods=len(user_prod_basket)))


async def order_yes(callback_query: types.CallbackQuery):
    db.bd_del_from_the_basket_no_verified(callback_query.from_user.id)
    db.bd_changes_count_in_basket_count_stock(callback_query.from_user.id)
    await order_formation(callback_query.from_user.id)


async def order_no(callback_query: types.CallbackQuery):
    await callback_query.message.delete()


async def order_formation(user_id):
    user_prod = db.bd_product_for_user_in_the_basket_availability(user_id)
    order_quantity = []
    for prod in user_prod:
        full_prod = db.bd_returns_one_item(int(prod[1]))
        order_quantity.append(str(prod[1]) + ':' + str(full_prod[4]) + ':' +
                              str(prod[3]) + ':'
                              + str(full_prod[6]))

    date_new = datetime.today()
    amount = map(lambda x: float(x.split(':')[3]) * int(x.split(':')[2]), order_quantity)
    db.bd_add_product_in_orders((user_id, date_new.strftime("%d.%m.%Y"), date_new.strftime("%H.%M.%S"),
                                 (',').join(order_quantity), sum(amount)))
    for product in user_prod:
        db.bd_changes_count_in_stock(product[3], product[1])
    db.bd_del_all_basket_from_user(user_id)
    order = db.bd_id_order(user_id)  # последний заказ пользователя

    order_product = [i.split(':') for i in order[4].split(',')]
    a = ''
    for j in order_product:
        a += f'<b>{j[1]}</b> - {j[2]} шт. ({j[3]} руб/шт.)\n'
    await bot.send_message(user_id, text=f'<b>Ваш Заказ №{order[0]}</b>\n******\n{a}******\n<b>Сумма: {order[5]} руб.</b>\nОтправлен на сборку,\n'
                                         f'Пожалуйста дождитесь сообщения о готовности',
                           parse_mode='HTML', reply_markup=keyboard_user)
    await bot.send_message(ADMIN_ID, text=f'<b>Новый заказ №{order[0]}</b>\n{a}<b>Сумма: {order[5]} руб.</b>',
                           parse_mode='HTML', reply_markup=InlineKeyboardMarkup().
                           add(InlineKeyboardButton(f'Готов',
                                                    callback_data=f"is_ready:{order[0]}")).
                           add(InlineKeyboardButton('Подробнее', callback_data=f"null"),
                               InlineKeyboardButton('Сообщение', callback_data=f"null")))


def register_handler_order(dp: Dispatcher):
    dp.register_callback_query_handler(buy_step1, lambda x: x.data.startswith('buy'))
    dp.register_callback_query_handler(next_order, lambda x: x.data.startswith('next_order'))
    dp.register_callback_query_handler(order_yes, lambda x: x.data.startswith('yes_buy'))
    dp.register_callback_query_handler(order_no, lambda x: x.data.startswith('no_buy'))
