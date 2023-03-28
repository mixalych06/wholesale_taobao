from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputFile

"""
      Кнопки для корзины если в корзине более наменования принимает:
      prod - id текущего продукта,
      number=0 - порядковый номер текущего продукта,
      lot=0 - количество данного товара в корзине,
      len_goods_in_basket=0 - количество наименований товаров в корзине, *args, **kwargs
      Отдаёт инлайн клавиатуру"""


async def repl_for_basket(user_id, prod, number=0, lot=0, len_goods_in_basket=0):
    repl = InlineKeyboardMarkup(row_width=4)
    if number == 0:
        repl.add(InlineKeyboardButton(
            f'В корзине:{lot} шт.', callback_data=f"null")).add(
            InlineKeyboardButton('⬅️⬅️⬅️', callback_data=f'next_basket:{len_goods_in_basket - 1}'),
            InlineKeyboardButton(f'{number + 1}/{len_goods_in_basket}', callback_data='null'),
            InlineKeyboardButton('❌', callback_data=f'del_basket:{prod}:{number}'),
            InlineKeyboardButton('➡️➡️➡️', callback_data=f'next_basket:{number + 1}')).add(
            InlineKeyboardButton('Купить', callback_data=f"buy:{user_id}"))
    elif number == len_goods_in_basket - 1:
        repl.add(InlineKeyboardButton(
            f'В корзине: {lot} шт.', callback_data=f"null")).add(
            InlineKeyboardButton('⬅️⬅️⬅️', callback_data=f'next_basket:{number - 1}'),
            InlineKeyboardButton(f'{number + 1}/{len_goods_in_basket}', callback_data='null'),
            InlineKeyboardButton('❌', callback_data=f'del_basket:{prod}:{number}'),
            InlineKeyboardButton('➡️➡️➡️', callback_data=f'next_basket:{0}')).add(
            InlineKeyboardButton('Купить', callback_data=f"buy:{user_id}"))
    elif 0 < number < len_goods_in_basket - 1:
        repl.add(InlineKeyboardButton(
            f'В корзине: {lot} шт.', callback_data=f"null")).add(
            InlineKeyboardButton('⬅️⬅️⬅️', callback_data=f'next_basket:{number - 1}'),
            InlineKeyboardButton(f'{number + 1}/{len_goods_in_basket}', callback_data='null'),
            InlineKeyboardButton('❌', callback_data=f'del_basket:{prod}:{number}'),
            InlineKeyboardButton('➡️➡️➡️', callback_data=f'next_basket:{number + 1}')).add(
            InlineKeyboardButton('Купить', callback_data=f"buy:{user_id}"))
    return repl
