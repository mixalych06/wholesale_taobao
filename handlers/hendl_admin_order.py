from create_bot import bot, db
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputFile
from create_bot import ADMIN_ID
from keyboards.kb_user import keyboard_user
from keyboards.kb_admin import keyboard_order_admin


async def order_is_ready(callback: types.CallbackQuery):
    """Обрабатывает кнопку админа готов при собраном заказе"""
    inline_command = callback.data.split(':')
    db.bd_order_is_ready(int(inline_command[1]))
    user_id = db.bd_return_id_user_from_the_order(int(inline_command[1]))
    await bot.send_message(chat_id=user_id,
                           text=f'Ваш заказ №{inline_command[1]} готов к выдаче, для получения свяжитесь с \n'
                                f'<a href="https://t.me/mixalych06">администратором</a>', parse_mode='HTML',
                           reply_markup=keyboard_user)
    await callback.answer(f'Заказ {inline_command[1]} собран и готов к выдаче')
    await callback.message.delete()


async def admin_menu_orders(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.chat.id, text='Выбери категорию заказа', reply_markup=keyboard_order_admin)


async def admin_not_ready_orders(message: types.Message):
    """Выдаёт админу не собраные заказы"""
    await bot.delete_message(message.chat.id, message.message_id)
    orders = db.bd_all_not_ready_order()
    if orders:
        for order in orders:
            order_product = [i.split(':') for i in order[4].split(',')]
            a = ''
            for j in order_product:
                a += f'<b>{j[1]}</b> - {j[2]} шт. ({j[3]} руб/шт.)\n'
            await bot.send_message(message.from_user.id, text=f'Заказ №{order[0]}\n{a}Сумма {order[5]} руб.',
                                   parse_mode='HTML', reply_markup=InlineKeyboardMarkup().
                                   add(InlineKeyboardButton(f'Готов',
                                                            callback_data=f"is_ready:{order[0]}")).
                                   add(InlineKeyboardButton('Подробнее', callback_data=f"null"),
                                       InlineKeyboardButton('Сообщение', callback_data=f"null")))
    else:
        await bot.send_message(message.from_user.id, text=f'Все заказы собраны и готовы к выдаче',
                               parse_mode='HTML')


async def admin_ready_orders(message: types.Message):
    """Выдаёт админу готовые к выдаче заказы"""
    await bot.delete_message(message.chat.id, message.message_id)
    orders = db.bd_all_ready_order()
    if orders:
        for order in orders:
            order_product = [i.split(':') for i in order[4].split(',')]
            a = ''
            for j in order_product:
                a += f'<b>{j[1]}</b> - {j[2]} шт. ({j[3]} руб/шт.)\n'
            await bot.send_message(message.from_user.id, text=f'Заказ №{order[0]}\n{a}Сумма {order[5]} руб.',
                                   parse_mode='HTML', reply_markup=InlineKeyboardMarkup().
                                   add(InlineKeyboardButton(f'Выдан',
                                                            callback_data=f"issued:{order[0]}")).
                                   add(InlineKeyboardButton('Подробнее', callback_data=f"null"),
                                       InlineKeyboardButton('Сообщение', callback_data=f"null")))
    else:
        await bot.send_message(message.from_user.id, text=f'Нет заказов готовых к выдаче',
                               parse_mode='HTML')


async def admin_paid_for_orders(message: types.Message):
    pass


async def order_is_issued(callback: types.CallbackQuery):
    """Обрабатывает кнопку админа готов при собраном заказе"""
    inline_command = callback.data.split(':')
    db.bd_order_is_issued(int(inline_command[1]))
    await callback.answer(f'Заказ {inline_command[1]} оплачен и выдан')
    await callback.message.delete()


def register_hendl_admin_order(dp: Dispatcher):
    dp.register_callback_query_handler(order_is_issued, lambda x: x.data.startswith('issued'))
    dp.register_callback_query_handler(order_is_ready, lambda x: x.data.startswith('is_ready'))
    dp.register_message_handler(admin_menu_orders, lambda message: str(message.from_user.id) in ADMIN_ID,
                                text='Заказы')
    dp.register_message_handler(admin_not_ready_orders, lambda message: str(message.from_user.id) in ADMIN_ID,
                                text='На сборке')
    dp.register_message_handler(admin_ready_orders, lambda message: str(message.from_user.id) in ADMIN_ID,
                                text='К выдаче')
    dp.register_message_handler(admin_paid_for_orders, lambda message: str(message.from_user.id) in ADMIN_ID,
                                text='Оплаченые')
