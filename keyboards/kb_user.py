from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard_user: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)

but_user_products_in_stock: KeyboardButton = KeyboardButton('Товары в наличии')
but_user_basket: KeyboardButton = KeyboardButton('🛒Корзина')
but_help: KeyboardButton = KeyboardButton('🆘Помощь')
keyboard_user.add(but_user_products_in_stock, but_user_basket).add(but_help)


