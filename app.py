import configparser
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from handlers.message_handler import register_message_handler
from handlers.inline_handler import register_inline_handler
from handlers.callback_handler import register_callback_handler


async def set_commands(bot: Bot):
    commands = [BotCommand(command="/start", description="Search Music")]
    await bot.set_my_commands(commands)


async def main():
    # Парсинг файла конфигурации
    config = configparser.ConfigParser()
    config.read('setting.ini')

    # Инициализация объектов bot и dispatcher
    bot = Bot(token=config.get('Telegram', 'token'))
    dp = Dispatcher(bot)

    # Регистрация хэндлеров
    register_message_handler(dp)
    register_inline_handler(dp)
    register_callback_handler(dp)

    # Регистрация команд бота
    await set_commands(bot)

    # Запуск поллинга
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())