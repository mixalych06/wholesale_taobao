from create_bot import bot, db
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from keyboards.kb_basket import repl_for_basket


async def user_basket(message: types.Message):
    """Открытие корзины"""
    all_product_for_user = db.bd_all_product_for_user_in_the_basket(message.from_user.id)
    if all_product_for_user:
        await bot.send_message(message.chat.id, f'В корзине {len(all_product_for_user)} товаров.',
                               reply_markup=InlineKeyboardMarkup().
                               add(InlineKeyboardButton('Подробнее', callback_data=f'cart_details:0')))
    else:
        await bot.send_message(message.chat.id, 'Корзина пустая')


async def basket_details_user(callback: types.CallbackQuery):
    inline_command = callback.data.split(':')
    number = int(inline_command[1])
    all_product_for_user = db.bd_all_product_for_user_in_the_basket(callback.from_user.id)

    try:
        prod = db.bd_returns_one_item(all_product_for_user[number][1])
        print(prod)
        await callback.message.delete()
    except IndexError:
        await callback.message.delete()
        await bot.send_message(callback.message.chat.id, 'Корзина пустая')
        return

    if len(all_product_for_user) == 1:
        await callback.bot.send_photo(callback.from_user.id, photo=prod[3],
                                      caption=f"<b>{prod[4].strip().upper()}</b>\n{prod[5]}\n<b>Цена: </b>{prod[6]}",
                                      parse_mode='HTML',
                                      reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                          f'В корзине: {all_product_for_user[number][2]} шт.', callback_data=f"null")).
                                      add(InlineKeyboardButton(
                                          '❌', callback_data=f'del_basket:{prod[0]}:{number}'),
                                          InlineKeyboardButton('Купить', callback_data=f"buy:{callback.from_user.id}")))

    elif len(all_product_for_user) > 1:
        await callback.bot.send_photo(callback.from_user.id, photo=prod[3],
                                      caption=f'<b>{prod[4].strip().upper()}</b>\n{prod[5]}\n<b>Цена: </b>{prod[6]}',
                                      parse_mode='HTML',
                                      reply_markup=await repl_for_basket(callback.from_user.id, prod=prod[0],
                                                                         number=number,
                                                                         lot=all_product_for_user[number][2],
                                                                         len_goods_in_basket=len(all_product_for_user)))


async def basket_next_user(callback: types.CallbackQuery):
    inline_command = callback.data.split(':')
    number = int(inline_command[1])
    all_product_for_user = db.bd_all_product_for_user_in_the_basket(callback.from_user.id)
    prod = db.bd_returns_one_item(all_product_for_user[number][1])
    user_caption = f'<b>{prod[4].strip().upper()}</b>\n{prod[5]}\n<b>Цена: </b>{prod[6]}'
    photo = InputMediaPhoto(media=prod[3], caption=user_caption, parse_mode='HTML')
    if len(all_product_for_user) == 1:
        await callback.bot.edit_message_media(media=photo, chat_id=callback.message.chat.id,
                                              message_id=callback.message.message_id,
                                              reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                                  f'В корзине: {all_product_for_user[number][2]} шт.',
                                                  callback_data=f"null")).
                                              add(InlineKeyboardButton(
                                                  '❌', callback_data=
                                                  f'del_basket:{prod[0]}:{number}'),
                                                  InlineKeyboardButton('Купить', callback_data=
                                                  f"buy:{callback.from_user.id}")))
    elif len(all_product_for_user) > 1:
        await callback.bot.edit_message_media(media=photo, chat_id=callback.message.chat.id,
                                              message_id=callback.message.message_id,
                                              reply_markup=await repl_for_basket(callback.from_user.id,
                                                                                 prod=prod[0], number=number,
                                                                                 lot=all_product_for_user[number][2],
                                                                                 len_goods_in_basket=len(
                                                                                     all_product_for_user)))


async def dell_product_from_the_basket(callback: types.CallbackQuery):
    inline_command = callback.data.split(':')
    count = db.bd_checks_product_in_the_basket(callback.from_user.id, int(inline_command[1]))
    if count and count[0][0] > 1:
        db.bd_del_from_the_basket(1, callback.from_user.id, inline_command[1])
        number = int(inline_command[2])
        all_product_for_user = db.bd_all_product_for_user_in_the_basket(callback.from_user.id)
        prod = db.bd_returns_one_item(all_product_for_user[number][1])
        if len(all_product_for_user) == 1:
            await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(f'В корзине: {all_product_for_user[number][2]} шт.', callback_data=f"null")).add(
                InlineKeyboardButton('❌', callback_data=f'del_basket:{all_product_for_user[number][1]}:{number}'),
                InlineKeyboardButton('Купить', callback_data=f"buy:{callback.from_user.id}")))
        elif len(all_product_for_user) > 1:
            await callback.message.edit_reply_markup(reply_markup=await repl_for_basket(callback.from_user.id,
                                                                                        prod=prod[0], number=number,
                                                                                        lot=
                                                                                        all_product_for_user[number][2],
                                                                                        len_goods_in_basket=len(
                                                                                            all_product_for_user)))
    else:
        db.bd_del_from_the_basket(0, callback.from_user.id, inline_command[1])
        all_product_for_user = db.bd_all_product_for_user_in_the_basket(callback.from_user.id)
        if not all_product_for_user:
            await callback.answer('Корзина пустая', show_alert=True)
            await callback.message.delete()
            return
        try:
            number = int(inline_command[2])
            prod = db.bd_returns_one_item(all_product_for_user[number][1])
        except:
            number = int(inline_command[2]) - 1
            all_product_for_user = db.bd_all_product_for_user_in_the_basket(callback.from_user.id)
            prod = db.bd_returns_one_item(all_product_for_user[number][1])
        user_caption = f'<b>{prod[4].strip().upper()}</b>\n{prod[5]}\n<b>Цена: </b>{prod[6]}'
        photo = InputMediaPhoto(media=prod[3], caption=user_caption, parse_mode='HTML')
        if len(all_product_for_user) == 1:
            await callback.bot.edit_message_media(media=photo, chat_id=callback.message.chat.id,
                                                  message_id=callback.message.message_id,
                                                  reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                                                      f'В корзине: {all_product_for_user[number][2]} шт.',
                                                      callback_data=f"null")).
                                                  add(InlineKeyboardButton(
                                                      '❌', callback_data=
                                                      f'del_basket:{prod[0]}:{number}'),
                                                      InlineKeyboardButton('Купить', callback_data=
                                                      f'buy:{callback.from_user.id}')))
        elif len(all_product_for_user) > 1:
            await callback.bot.edit_message_media(media=photo, chat_id=callback.message.chat.id,
                                                  message_id=callback.message.message_id,
                                                  reply_markup=await repl_for_basket(callback.from_user.id,
                                                                                     prod=prod[0], number=number,
                                                                                     lot=all_product_for_user[number][
                                                                                         2],
                                                                                     len_goods_in_basket=len(
                                                                                         all_product_for_user)))


def register_handler_basket(dp: Dispatcher):
    dp.register_message_handler(user_basket, text='🛒Корзина')
    dp.register_callback_query_handler(basket_details_user, lambda x: x.data.startswith('cart_details'))
    dp.register_callback_query_handler(basket_next_user, lambda x: x.data.startswith('next_basket'))
    dp.register_callback_query_handler(dell_product_from_the_basket, lambda x: x.data.startswith('del_basket'))
