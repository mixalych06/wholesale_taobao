from create_bot import bot, db
from aiogram.dispatcher import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


async def cancel_fsm(callback_query: types.CallbackQuery, state: FSMContext):
    '''Отмена ввода обьявления, сброс машины состояния'''
    await state.reset_state()
    inline_command = callback_query.data
    await callback_query.answer(
        text='Отменено',
        show_alert=True)
    await callback_query.message.delete()


def register_handler_other(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_fsm, lambda x: x.data.startswith('cancel'), state='*')
