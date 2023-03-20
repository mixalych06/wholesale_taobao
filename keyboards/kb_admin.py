from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.kb_user import but_help

keyboard_admin1: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)

but_edit_products: KeyboardButton = KeyboardButton('Редактировать товары')
but_add_product: KeyboardButton = KeyboardButton('Добавить товар')
but_add_category: KeyboardButton = KeyboardButton('Добавить страну')
but_category: KeyboardButton = KeyboardButton('Добавить категорию')
keyboard_admin1.add(but_edit_products, but_add_product).add(but_add_category, but_category).add(but_help)
