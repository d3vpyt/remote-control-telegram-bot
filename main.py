import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram.utils.callback_data import CallbackData

bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot)
keyboards_query = CallbackData('keyboard', 'action', 'value')


def create_menu_keyboard():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton('🌗 Перезагрузка',
                             callback_data=keyboards_query.new(action='remote_control', value='reboot')),
        InlineKeyboardButton('➕ Громкость', callback_data=keyboards_query.new(action='remote_control',
                                                                              value='amixer -D pulse sset Master 10%+')),
        InlineKeyboardButton('🌙 Выключение',
                             callback_data=keyboards_query.new(action='remote_control',
                                                               value='shutdown -P 0.30')),
        InlineKeyboardButton('➖ Громкость', callback_data=keyboards_query.new(action='remote_control',
                                                                              value='amixer -D pulse sset Master 10%-'))
    )


@dp.message_handler(commands='start')
async def select_report(message: types.Message):
    await bot.send_message(message.chat.id, 'Выберите действие', reply_markup=create_menu_keyboard())


@dp.callback_query_handler(keyboards_query.filter(action='remote_control'))
async def send_repo(query: types.CallbackQuery, callback_data: dict):
    os.system(callback_data['value'])


if __name__ == '__main__':
    executor.start_polling(dp)
