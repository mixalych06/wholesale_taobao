from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputFile

keyboard_user: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)

but_user_products_in_stock: KeyboardButton = KeyboardButton('Товары в наличии')
but_user_basket: KeyboardButton = KeyboardButton('🛒Корзина')
but_help: KeyboardButton = KeyboardButton('🆘Помощь')
keyboard_user.add(but_user_products_in_stock, but_user_basket).add(but_help)

"""
      Кнопки для корзины если в корзине более наменования принимает:
      prod - количество продуктов для показа,
      number=0 - порядковый номер текущего продукта,
      id_prod =0 - id текущего продукта,
      len_goods_in_basket=0 - количество наименований товаров в корзине, *args, **kwargs
      Отдаёт инлайн клавиатуру"""


async def repl_for_categor(prod, id_prod, category, komand, number=0):
    """Создает кнопки пагинации для товаров в наличии в зависимости от порядкового номера текущего товара"""
    repl = InlineKeyboardMarkup(row_width=4)
    if 0 < number < prod - 1:
        repl.add(InlineKeyboardButton(f'{number + 1}/{prod}', callback_data='null')).add(
            InlineKeyboardButton('⬅️⬅️⬅️', callback_data=f'next_u:{category}:{komand}:{number - 1}'),
            InlineKeyboardButton('➡️➡️➡️', callback_data=f'next_u:{category}:{komand}:{number + 1}')).add(
            InlineKeyboardButton('В корзину', callback_data=f'add_basket:{id_prod}'))
    elif number == 0:
        repl.add(InlineKeyboardButton(f'{number + 1}/{prod}', callback_data='null')).add(
            InlineKeyboardButton('⬅️⬅️⬅️', callback_data=f'next_u:{category}:{komand}:{prod - 1}'),
            InlineKeyboardButton('➡️➡️➡️', callback_data=f'next_u:{category}:{komand}:{number + 1}')).add(
            InlineKeyboardButton('В корзину', callback_data=f'add_basket:{id_prod}'))
    elif number == prod - 1:
        repl.add(InlineKeyboardButton(f'{number + 1}/{prod}', callback_data='null')).add(
            InlineKeyboardButton('⬅️⬅️⬅️', callback_data=f'next_u:{category}:{komand}:{number - 1}'),
            InlineKeyboardButton('➡️➡️➡️', callback_data=f'next_u:{category}:{komand}:{0}')).add(
            InlineKeyboardButton('В корзину', callback_data=f'add_basket:{id_prod}'))
    return repl
