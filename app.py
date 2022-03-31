from utils.misc.logging import logger

from aiogram.utils import executor

from loader import dp
import middlewares, filters, handlers
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    logger.info("Ожидание команды")
    await set_default_commands(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)



