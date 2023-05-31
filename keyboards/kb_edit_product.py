from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


"""
      Кнопки для корзины если в корзине более наменования принимает:
      prod - количество продуктов для показа,
      number=0 - порядковый номер текущего продукта,
      id_prod =0 - id текущего продукта,
      len_goods_in_basket=0 - количество наименований товаров в корзине, *args, **kwargs
      Отдаёт инлайн клавиатуру"""


async def repl_for_categor_for_admin(prod, id_prod, category, country, number=0):
    """Создает кнопки пагинации для товаров в наличии в зависимости от порядкового номера текущего товара"""
    repl = InlineKeyboardMarkup(row_width=4)
    if 0 < number < prod - 1:
        repl.add(
            InlineKeyboardButton("➕", callback_data=f'plus:{id_prod}:{prod}:{number}:{-1}'),
            InlineKeyboardButton("➖", callback_data=f'plus:{id_prod}:{prod}:{number}:{1}')).add(
            InlineKeyboardButton("Редактировать товар", callback_data=f'edit_product:{id_prod}')).add(
            InlineKeyboardButton('⬅️⬅️⬅️', callback_data=f'next_a:{country}:{category}:{number - 1}'),
            InlineKeyboardButton(f'{number + 1}/{prod}', callback_data='null'),
            InlineKeyboardButton('➡️➡️➡️', callback_data=f'next_a:{country}:{category}:{number + 1}')).add(
            InlineKeyboardButton('Удалить', callback_data=f'delprod:{id_prod}'),
            InlineKeyboardButton('Назад', callback_data=f'catforad:{country}'))
    elif number == 0:
        repl.add(
            InlineKeyboardButton("➕", callback_data=f'plus:{id_prod}:{prod}:{number}:{-1}'),
            InlineKeyboardButton("➖", callback_data=f'plus:{id_prod}:{prod}:{number}:{1}')).add(
            InlineKeyboardButton("Редактировать товар", callback_data=f'edit_product:{id_prod}')).add(
            InlineKeyboardButton('⬅️⬅️⬅️', callback_data=f'next_a:{country}:{category}:{prod - 1}'),
            InlineKeyboardButton(f'{number + 1}/{prod}', callback_data='null'),
            InlineKeyboardButton('➡️➡️➡️', callback_data=f'next_a:{country}:{category}:{number + 1}')).add(
            InlineKeyboardButton('Удалить', callback_data=f'delprod:{id_prod}'),
            InlineKeyboardButton('Назад', callback_data=f'catforad:{country}'))
    elif number == prod - 1:
        repl.add(
            InlineKeyboardButton("➕", callback_data=f'plus:{id_prod}:{prod}:{number}:{-1}'),
            InlineKeyboardButton("➖", callback_data=f'plus:{id_prod}:{prod}:{number}:{1}')).add(
            InlineKeyboardButton("Редактировать товар", callback_data=f'edit_product:{id_prod}')).add(
            InlineKeyboardButton('⬅️⬅️⬅️', callback_data=f'next_a:{country}:{category}:{number - 1}'),
            InlineKeyboardButton(f'{number + 1}/{prod}', callback_data='null'),
            InlineKeyboardButton('➡️➡️➡️', callback_data=f'next_a:{country}:{category}:{0}')).add(
            InlineKeyboardButton('Удалить', callback_data=f'delprod:{id_prod}'),
            InlineKeyboardButton('Назад', callback_data=f'catforad:{country}'))
    return repl