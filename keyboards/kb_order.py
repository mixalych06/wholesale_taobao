from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def repl_for_order(user_id, number=0, lot=0, len_goods=0):
    repl = InlineKeyboardMarkup(row_width=4)
    if number == 0:
        repl.add(InlineKeyboardButton(
            f'Заказ:{lot} шт.', callback_data=f"null")).add(
            InlineKeyboardButton('⬅️⬅️⬅️', callback_data=f'next_order:{len_goods - 1}'),
            InlineKeyboardButton(f'{number + 1}/{len_goods}', callback_data='null'),
            InlineKeyboardButton('➡️➡️➡️', callback_data=f'next_order:{number + 1}')).add(
            InlineKeyboardButton('Купить', callback_data=f"yes_buy:{user_id}"),
            InlineKeyboardButton('Отмена', callback_data=f"no_buy:{user_id}"))
    elif number == len_goods - 1:
        repl.add(InlineKeyboardButton(
            f'Заказ: {lot} шт.', callback_data=f"null")).add(
            InlineKeyboardButton('⬅️⬅️⬅️', callback_data=f'next_order:{number - 1}'),
            InlineKeyboardButton(f'{number + 1}/{len_goods}', callback_data='null'),
            InlineKeyboardButton('➡️➡️➡️', callback_data=f'next_order:{0}')).add(
            InlineKeyboardButton('Купить', callback_data=f"yes_buy:{user_id}"),
            InlineKeyboardButton('Отмена', callback_data=f"no_buy:{user_id}"))
    elif 0 < number < len_goods - 1:
        repl.add(InlineKeyboardButton(
            f'Заказ: {lot} шт.', callback_data=f"null")).add(
            InlineKeyboardButton('⬅️⬅️⬅️', callback_data=f'next_order:{number - 1}'),
            InlineKeyboardButton(f'{number + 1}/{len_goods}', callback_data='null'),
            InlineKeyboardButton('➡️➡️➡️', callback_data=f'next_order:{number + 1}')).add(
            InlineKeyboardButton('Купить', callback_data=f"yes_buy:{user_id}"),
            InlineKeyboardButton('Отмена', callback_data=f"no_buy:{user_id}"))
    return repl
