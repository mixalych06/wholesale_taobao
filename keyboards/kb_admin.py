from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.kb_user import but_help

keyboard_admin1: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_order_admin: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)

but_edit_products: KeyboardButton = KeyboardButton('Редактировать товары')
but_add_product: KeyboardButton = KeyboardButton('Добавить товар')
but_add_category: KeyboardButton = KeyboardButton('Добавить страну')
but_category: KeyboardButton = KeyboardButton('Добавить категорию')
but_admin_orders: KeyboardButton = KeyboardButton('Заказы')
keyboard_admin1.add(but_admin_orders).add(but_edit_products, but_add_product).add(but_add_category, but_category).add(but_help)

but_not_ready: KeyboardButton = KeyboardButton('На сборке')
but_ready: KeyboardButton = KeyboardButton('К выдаче')
but_paid_for: KeyboardButton = KeyboardButton('Оплаченые')
but_main_menu: KeyboardButton = KeyboardButton('Назад')
keyboard_order_admin.add(but_not_ready).add(but_ready).add(but_paid_for).add(but_main_menu)
