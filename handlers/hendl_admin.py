from create_bot import bot, db
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.kb_admin import keyboard_admin1
from keyboards.kb_other import gen_markup_category
from create_bot import ADMIN_ID


async def start_admin(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Привет, админ', reply_markup=keyboard_admin1)


class FSMRAddCountry(StatesGroup):
    country = State()


async def add_country_btn(message: types.Message):
    """Обработка кнопки добавить страну"""
    countries = db.bd_checks_for_country()
    country_dict = {country: 'red_count' for country in countries}
    country_dict['Добавить страну'] = 'add_count'
    country_dict['Отмена'] = "cancel"
    await bot.send_message(message.from_user.id, text='Выберите страну для редактирования или добавьте новую',
                           reply_markup=await gen_markup_category(country_dict))


async def start_fsm_add_country(callback_query: types.CallbackQuery):
    """Обработка инлайн кнопки добавить страну Старт FSMAddCountry"""
    await callback_query.message.reply('Введите страну',
                                       reply_markup=InlineKeyboardMarkup().add(
                                           InlineKeyboardButton("Отмена", callback_data=f"cancel")))
    await FSMRAddCountry.country.set()


async def add_country(message: types.Message, state: FSMContext):
    """Завершение FSMAddCountry. Запись в БД новой страны"""
    db.bd_add_country(message.text.strip().capitalize())
    await state.finish()
    countries = db.bd_checks_for_country()
    country_dict = {country: 'red_count' for country in countries}
    country_dict['Добавить страну'] = 'add_count'
    country_dict['Отмена'] = "cancel"
    await bot.send_message(message.from_user.id, text='Выберите страну для редактирования или добавьте новую',
                           reply_markup=await gen_markup_category(country_dict))


class FSMRAddCategories(StatesGroup):
    categories = State()


async def add_categories_btn(message: types.Message):
    """Обработка кнопки добавить категории"""
    categories = db.bd_checks_for_categories()
    categories_dict = {category: 'red_categor' for category in categories}
    categories_dict['Добавить категории'] = 'add_categor'
    categories_dict['Отмена'] = "cancel"
    await bot.send_message(message.from_user.id, text='Выберите категорию для редактирования или добавьте новые',
                           reply_markup=await gen_markup_category(categories_dict))


async def start_fsm_add_categories(callback_query: types.CallbackQuery):
    """Обработка инлайн кнопки добавить категорию Старт FSMAddCategories"""
    await callback_query.message.reply('Введите категорию или несколько через запятую',
                                       reply_markup=InlineKeyboardMarkup().add(
                                           InlineKeyboardButton("Отмена", callback_data=f"cancel")))
    await FSMRAddCategories.categories.set()


async def add_categories(message: types.Message, state: FSMContext):
    """Завершение FSMAddCategories. Запись в БД новой категории"""
    db.bd_add_category([c.strip() for c in message.text.split(',') if c])
    await state.finish()
    categories = db.bd_checks_for_categories()
    categories_dict = {category: 'red_categor' for category in categories}
    categories_dict['Добавить категории'] = 'add_categor'
    categories_dict['Отмена'] = "cancel"
    await bot.send_message(message.from_user.id, text='Выберите категорию для редактирования или добавьте новые',
                           reply_markup=await gen_markup_category(categories_dict))


class FSMRAddProduct(StatesGroup):
    country = State()
    category = State()
    photo = State()
    product_name = State()
    specifications = State()
    prise = State()
    count = State()


async def add_product_start(message: types.Message):
    """Обработка  кнопки добавить товар/ Старт FSMAddProduct"""
    countries = db.bd_checks_for_country()
    country_dict = {country: 'add_prod_countr' for country in countries}
    country_dict['Отмена'] = "cancel"
    if countries:
        await bot.send_message(message.from_user.id, text='Выберите страну',
                               reply_markup=await gen_markup_category(country_dict))
        await FSMRAddProduct.country.set()
    else:
        await bot.send_message(message.from_user.id, text='Страны отсутствуют в БД добавьте с помощью кнопки'
                                                          '"Добавить страну')


async def add_product_counter(callback_query: types.CallbackQuery, state: FSMContext):
    inline_command = callback_query.data.split(':')
    async with state.proxy() as data:
        data['country'] = inline_command[1]
        await FSMRAddProduct.next()
        categories = db.bd_checks_for_categories()
        if categories:
            categories_dict = {category: 'add_prod_categor' for category in categories}
            categories_dict['Отмена'] = "cancel"
            await callback_query.message.reply(text='Выберите категорию',
                                               reply_markup=await gen_markup_category(categories_dict))
        else:
            await callback_query.message.answer(text='Нет категорий в базе, добавьте категорию')
            await state.reset_state()
            await callback_query.message.delete()


async def add_product_category(callback_query: types.CallbackQuery, state: FSMContext):
    inline_command = callback_query.data.split(':')
    async with state.proxy() as data:
        data['category'] = inline_command[1]
        await FSMRAddProduct.next()
        await callback_query.message.reply('Отправьте одно фото',
                                           reply_markup=InlineKeyboardMarkup().add(
                                               InlineKeyboardButton("Отмена", callback_data=f"cancel")))


async def add_product_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await FSMRAddProduct.next()
        await message.reply('Отправьте название', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Отмена", callback_data=f"cancel")))


async def add_product_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_name'] = message.text
        await FSMRAddProduct.next()
        await message.reply('Отправьте описание', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Отмена", callback_data=f"cancel")))


async def add_product_specifications(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['specifications'] = message.text
        await FSMRAddProduct.next()
        await message.reply('Отправьте цену', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Отмена", callback_data=f"cancel")))


async def add_product_prise(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['prise'] = message.text
        await FSMRAddProduct.next()
        await message.reply('Отправьте количество в наличии', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Отмена", callback_data=f"cancel")))


async def add_product_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['count'] = message.text
        db.bd_add_product_in_stock(list(data.values()))
        await message.answer(text='опубликовано')
        await state.finish()


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(start_admin, lambda message: str(message.from_user.id) in ADMIN_ID,
                                text=['Назад', '/startadministrator'])

    dp.register_message_handler(add_product_start, lambda message: str(message.from_user.id) in ADMIN_ID,
                                text='Добавить товар', state=None)
    dp.register_callback_query_handler(add_product_counter, lambda x: x.data.startswith('add_prod_countr'),
                                       state=FSMRAddProduct.country)
    dp.register_callback_query_handler(add_product_category, lambda x: x.data.startswith('add_prod_categor'),
                                       state=FSMRAddProduct.category)
    dp.register_message_handler(add_product_photo, content_types=['photo'], state=FSMRAddProduct.photo)
    dp.register_message_handler(add_product_product_name, state=FSMRAddProduct.product_name)
    dp.register_message_handler(add_product_specifications, state=FSMRAddProduct.specifications)
    dp.register_message_handler(add_product_prise, state=FSMRAddProduct.prise)
    dp.register_message_handler(add_product_count, state=FSMRAddProduct.count)

    dp.register_message_handler(add_country_btn, lambda message: str(message.from_user.id) in ADMIN_ID,
                                text='Добавить страну')
    dp.register_callback_query_handler(start_fsm_add_country, lambda x: x.data.startswith('add_count'), state=None)
    dp.register_message_handler(add_country, state=FSMRAddCountry.country)

    dp.register_message_handler(add_categories_btn, lambda message: str(message.from_user.id) in ADMIN_ID,
                                text='Добавить категорию')
    dp.register_callback_query_handler(start_fsm_add_categories, lambda x: x.data.startswith('add_categor'), state=None)
    dp.register_message_handler(add_categories, state=FSMRAddCategories.categories)
