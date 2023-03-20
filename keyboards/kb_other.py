from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def gen_markup_category(categor: dict):
    """Создаёт инлайн клавиатуру из переданого словаря, ключ-список значений, знчение-для срабатывания хэндлера"""
    markup_categor = InlineKeyboardMarkup()
    x=[]
    for key, value in categor.items():
        x.append(InlineKeyboardButton(text=key, callback_data=f'{value}:{key}'))
    markup_categor.add(*x)
    return markup_categor
