from utils.misc.logging import logger
from aiogram import types
from utils.db_api.mysql import create_connection_mysql_db
from loader import dp
from aiogram.dispatcher.filters import Command
from data import config
from states.base_logic import MainLogic
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands='start')
async def bot_start(message: types.Message):
    logger.info("Старт")
    await message.answer("Мы начинаем")
    await MainLogic.ShowMessage.set()
    logger.info("Состояние просмотра сообщения")
    await message.answer("Готовы ?")


@dp.message_handler(state=MainLogic.ShowMessage)
async def show(message: types.Message, state: FSMContext):
    if message.text == 'Да' or message.text == 'да' or message.text == "1" or message.text == "2" or message.text == "3":
        await MainLogic.EditType.set()
        conn = await create_connection_mysql_db(config.MYSQL_HOST, config.MYSQL_USER, config.MYSQL_PASS)
        cursor = conn.cursor()
        logger.info("Успешное подключение к базе данных")

        async with state.proxy() as data:
            cursor.execute(f"""SELECT * FROM parse_tg.data_for_analysis WHERE type is NULL LIMIT 1;""")
            logger.info("Загрузка сообщения прошла успешно")
            data["message"] = [item for item in cursor.fetchall()]
            if len(data["message"]) == 0:
                return await message.answer("Нет сообщений")

        await message.answer(data["message"][0][2])
        await message.answer("Введите: \n 1 - Мусор \n 2 - Новости \n 3 - Сигнал")

        logger.info("Состояние ответа")

        cursor.close()
        conn.close()
    else:
        await message.answer("Введите да или нажмите кнопку отмены")


@dp.message_handler(state=MainLogic.EditType)
async def edit(message: types.Message, state: FSMContext):
    if message.text == "1" or message.text == "2" or message.text == "3":
        logger.info(f"Присвоенно {message.text}")

        conn = await create_connection_mysql_db(config.MYSQL_HOST, config.MYSQL_USER, config.MYSQL_PASS)
        cursor = conn.cursor()

        data = await state.get_data("message")
        id = data["message"][0][0]
        logger.info("Обновление записи")
        cursor.execute(f"""UPDATE parse_tg.data_for_analysis SET type ={int(message.text)} WHERE id = {id}""")

        logger.info(f"Обновление прошло успешно \n Сообщению с ID {id} присвоен тип {message.text}")
        await message.answer(f"Обновление прошло успешно \nСообщению с ID {id} присвоен тип {message.text}")
        cursor.close()
        conn.commit()
        conn.close()

        await MainLogic.ShowMessage.set()
        logger.info("Состояние просмотра сообщения")
        await show(message, state)
    else:
        await message.answer("Введите 1/2/3")



