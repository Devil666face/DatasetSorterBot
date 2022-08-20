import config

from aiogram import Bot,Dispatcher,types,executor
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from controller import Controller
from database import Database

from markup import Keyboards

# Костыль Globals
bot = Bot(token=config.TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

db = Database(db_file_name='database.db')
kb = Keyboards(db)
controller = Controller(db, kb, config.FIRST_FOLDER, config.SECOND_FOLDER)

@dp.message_handler(commands = ['make_admin'],state=None)
async def make_admin(message: types.Message):
    if db.make_admin(int(message.text.split()[1])):
        await message.answer(f'Права пользователя {int(message.text.split()[1])} изменены',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))
    else:
        await message.answer(f'Невозможно изменение прав пользователя {int(message.text.split()[1])}',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))
    

@dp.message_handler(commands = ['start'],state=None)
async def start(message: types.Message):
    if db.create_user(message=message):
        await message.answer(f'Вы добавлены в пользователи\nid = {message.from_user.id}\nname = {message.from_user.username}\nadmin = 0',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))
    else:
        await message.answer(f'Пользователь уже создан',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))


@dp.message_handler(Text(equals='Добавить фото в БД'))
async def indexing_db(message: types.Message, state: FSMContext):
    print(db.get_admin_id())
    if message.from_user.id in db.get_admin_id():
        await message.answer('Начинаю добавление новых фото в БД. Процесс займет много времени.',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))
        controller.indexing_db()
        await message.answer('Успешно!')
    else:
        await message.answer('У вас недостаточно прав для выполенния данных действий',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))


@dp.message_handler(Text(equals='Начать выдачу'))
async def help(message: types.Message, state: FSMContext):
    db.update_active_status(id=message.from_user.id,status=True)
    await message.answer('Начинаю выдачу датасета',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))
    photo_path, keyboard_inline = controller.get_question()
    if photo_path:
        await message.answer_photo(open(photo_path,'rb'),reply_markup=keyboard_inline)


@dp.callback_query_handler(text_contains="military_")
async def check(call: types.CallbackQuery):
    id = int(call.data.split('_')[2])
    controller.move_to_military(id)

@dp.callback_query_handler(text_contains="civil_")
async def check(call: types.CallbackQuery):
    id = int(call.data.split('_')[2])
    controller.move_to_civil(id)


@dp.callback_query_handler(text_contains="delete_")
async def check(call: types.CallbackQuery):
    id = int(call.data.split('_')[2])
    controller.delete(id)


@dp.message_handler(Text(equals='Остановить выдачу'))
async def help(message: types.Message, state: FSMContext):
    db.update_active_status(id=message.from_user.id,status=False)
    await message.answer('Выдача остановлена',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))


@dp.message_handler(Text(equals='Статистика'))
async def stat(message: types.Message, state: FSMContext):
    await message.answer('Заглушка Статистика',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))


@dp.message_handler(Text(equals='Помощь'))
async def help(message: types.Message, state: FSMContext):
    await message.answer('Заглушка Помощь',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))


@dp.message_handler(content_types=['text'],state=None)
async def not_response(message: types.Message, state:FSMContext):
    await message.answer('Я вас не понимаю',reply_markup=kb.keyboard_create_main_buttons(message.from_user.id))

if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)