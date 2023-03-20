from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


keyboard_user: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)

but_user_products_in_stock: KeyboardButton = KeyboardButton('Товары в наличии')
but_help: KeyboardButton = KeyboardButton('🆘Помощь')
keyboard_user.add(but_user_products_in_stock).add(but_help)


